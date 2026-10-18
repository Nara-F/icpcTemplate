#!/usr/bin/env python3
"""Build the icpcTemplate Markdown, self-contained HTML, and print-ready PDF."""
from __future__ import annotations
import argparse, html, json, re, shutil, subprocess, unicodedata
from xml.etree import ElementTree
from pathlib import Path
from html.parser import HTMLParser
from typst_pdf import build_typst, compile_pdf

ROOT = Path(__file__).resolve().parents[1]

def load_config():
    return json.loads((ROOT / "config/build.json").read_text(encoding="utf-8"))

def gather_sources(cfg):
    chapters = sorted(ROOT.glob(cfg["chapter_glob"]))
    extras = [ROOT / item for item in cfg.get("before_chapters", [])]
    after = [ROOT / item for item in cfg.get("after_chapters", [])]
    paths = extras + chapters + after
    missing = [p.relative_to(ROOT).as_posix() for p in paths if not p.is_file()]
    if missing: raise SystemExit("Missing configured source file(s): " + ", ".join(missing))
    if not chapters: raise SystemExit(f"No chapters found under {cfg['chapter_glob']}")
    return paths, chapters

def validate_sources(paths, chapters):
    explicit_ids=set()
    for path in chapters:
        text=path.read_text(encoding="utf-8")
        # Hash-prefixed lines in fenced shell/C++ examples are data, not
        # Markdown headings.
        prose=re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M|re.S)
        h1=re.findall(r"^#\s+(.+?)\s*$", prose, re.M)
        if len(h1) != 1:
            raise SystemExit(f"{path.relative_to(ROOT)}: expected exactly one chapter-level # heading")
        if not h1[0].strip(): raise SystemExit(f"{path}: empty chapter title")
        in_fence=False; fence_char=None; fence_len=0
        for number,line in enumerate(text.splitlines(),1):
            match=re.match(r"^\s*(`{3,}|~{3,})(.*)$",line)
            if match:
                marker,tail=match.groups()
                if not in_fence:
                    in_fence=True; fence_char=marker[0]; fence_len=len(marker)
                    lang=tail.strip()
                    if lang and not re.fullmatch(r"[A-Za-z0-9_+.-]+",lang):
                        raise SystemExit(f"{path}:{number}: invalid fenced code language {lang!r}")
                elif marker[0]==fence_char and len(marker)>=fence_len:
                    in_fence=False; fence_char=None; fence_len=0
                continue
            if not in_fence and re.match(r"^\s*\\newpage\s*$",line):
                raise SystemExit(f"{path}:{number}: stray \\newpage directive")
        if in_fence: raise SystemExit(f"{path}: unclosed fenced code block")
    for path in paths:
        text=path.read_text(encoding="utf-8")
        for offset,char in enumerate(text):
            if unicodedata.category(char) in {"Cc", "Cf"} and char not in "\t\n":
                line=text.count("\n",0,offset)+1
                column=offset-text.rfind("\n",0,offset)
                raise SystemExit(f"{path}:{line}:{column}: contains invisible control character U+{ord(char):04X}")
        if "\ufffd" in text: raise SystemExit(f"{path}: contains replacement character")
        for explicit_id in re.findall(r"\{#([A-Za-z][\w:.-]*)\}",text):
            if explicit_id in explicit_ids: raise SystemExit(f"{path}: duplicate explicit heading id {explicit_id!r}")
            explicit_ids.add(explicit_id)
    print(f"Validated {len(chapters)} chapters and {len(paths)-len(chapters)} supplemental source(s).")

def render(markdown_text, title, subtitle, language, css, template, toc_pages=None, page_placeholder=False):
    try:
        import markdown
    except ImportError as exc:
        raise SystemExit("Markdown dependencies missing. Run: python3 -m pip install -r requirements.txt") from exc
    md=markdown.Markdown(extensions=["extra", "sane_lists", "toc", "codehilite"], extension_configs={"toc":{"toc_depth":"1-2"},"codehilite":{"guess_lang":False,"linenums":False,"noclasses":False,"css_class":"highlight"}}, output_format="html5")
    body=md.convert(markdown_text)
    # Convert TeX math in text nodes only; fenced code remains byte-for-byte
    # intact. Pandoc is not needed at build time.
    try:
        from latex2mathml.converter import convert as tex_to_mathml
    except ImportError as exc:
        raise SystemExit("Math renderer missing. Run: python3 -m pip install -r requirements.txt") from exc
    chunks=re.split(r"(<[^>]+>)",body)
    code_depth=0
    inline=re.compile(r"(?<!\\)\$(?!\$)([^$\n]+?)(?<!\\)\$")
    display=re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$",re.S)
    for i,chunk in enumerate(chunks):
        if chunk.startswith("<"):
            if re.match(r"<(?:pre|code)(?:\s|>)",chunk): code_depth+=1
            elif re.match(r"</(?:pre|code)",chunk): code_depth=max(0,code_depth-1)
            continue
        if code_depth or not chunk: continue
        chunk=display.sub(lambda m:'<span class="math display">'+tex_to_mathml(html.unescape(m.group(1).strip()))+'</span>',chunk)
        chunk=inline.sub(lambda m:tex_to_mathml(html.unescape(m.group(1).strip())),chunk)
        chunks[i]=chunk
    body="".join(chunks)
    # CSS counters keep line numbers out of copied code text. Pygments emits
    # balanced spans per line; the final newline is not an extra source line.
    def code_lines(match):
        content=re.sub(r"^<span></span>", "", match.group(1))
        if content.startswith("<code>") and content.endswith("</code>"):
            content=content[6:-7]
        lines=content.removesuffix("\n").split("\n")
        return "<pre><code>"+"\n".join('<span class="code-line"><span class="code-text">'+line+'</span></span>' for line in lines)+"</code></pre>"
    body=re.sub(r"<pre>(.*?)</pre>",code_lines,body,flags=re.S)
    def render_toc(tokens):
        items=["<ol>"]
        for token in tokens:
            anchor=html.escape(token["id"],quote=True)
            label=token.get("html") or html.escape(token["name"])
            page=str((toc_pages or {}).get(token["id"],"000" if page_placeholder else ""))
            page_cell=f'<span class="toc-page">{html.escape(page)}</span>' if page or page_placeholder else ""
            items.append(f'<li><a href="#{anchor}"><span class="toc-label">{label}</span><span class="toc-leader"></span>{page_cell}</a>')
            if token.get("children"): items.append(render_toc(token["children"]))
            items.append("</li>")
        items.append("</ol>")
        return "\n".join(items)
    toc=render_toc(md.toc_tokens)
    source=template.read_text(encoding="utf-8")
    replacements={"language":html.escape(language, quote=True),"title":html.escape(title),"subtitle":html.escape(subtitle),"css":css,"toc":toc,"body":body}
    for key,value in replacements.items(): source=source.replace("{{ "+key+" }}",value)
    return source

class LinksAndIds(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.fragments=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs: self.ids.add(attrs["id"])
        if tag=="a" and attrs.get("href","").startswith("#"):
            self.fragments.append(attrs["href"][1:])

def validate_html(page, markdown_text):
    parser=LinksAndIds(); parser.feed(page)
    missing=sorted(set(parser.fragments)-parser.ids)
    if missing: raise SystemExit("Broken in-document links: " + ", ".join(missing))
    expected_code=len(re.findall(r"^```",markdown_text,re.M))//2
    actual_code=page.count("<pre>")
    if actual_code != expected_code:
        raise SystemExit(f"Code preservation check failed: {expected_code} fenced blocks, rendered {actual_code}")

def validate_pdf_bounds(pdf_path, expected_pages):
    raw=subprocess.run(["pdftotext","-bbox",str(pdf_path),"-"],check=True,text=True,capture_output=True).stdout
    tree=ElementTree.fromstring(raw[raw.index("<html"):])
    ns={"x":"http://www.w3.org/1999/xhtml"}
    pages=tree.findall(".//x:page",ns)
    if len(pages)!=expected_pages: raise SystemExit("PDF bbox validation failed: page count differs from pdfinfo")
    for number,page in enumerate(pages,1):
        width=float(page.get("width")); height=float(page.get("height")); words=page.findall("./x:word",ns)
        if len(words)<3: raise SystemExit(f"PDF layout validation failed: page {number} is nearly empty")
        for word in words:
            x0,y0,x1,y1=(float(word.get(key)) for key in ("xMin","yMin","xMax","yMax"))
            if x0<35 or x1>width-35 or y0<25 or y1>height-10:
                raise SystemExit(f"PDF layout validation failed: text near/outside page boundary on page {number}: {word.text!r}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--validate-only",action="store_true")
    parser.add_argument("--format",choices=("markdown","html","typst","pdf","all"),default="all",help="choose which independent export layers to build")
    parser.add_argument("--html-only",action="store_true",help="compatibility alias for --format html")
    args=parser.parse_args()
    cfg=load_config(); sources,chapters=gather_sources(cfg); validate_sources(sources,chapters)
    if args.validate_only:return
    markdown_text="\n\n".join(re.sub(r"^\s*\\newpage\s*$", "", p.read_text(encoding="utf-8").rstrip(), flags=re.M) for p in sources)+"\n"
    md_path=ROOT/cfg["markdown"]; html_path=ROOT/cfg["html"]; pdf_path=ROOT/cfg["pdf"]
    md_path.parent.mkdir(parents=True,exist_ok=True); html_path.parent.mkdir(parents=True,exist_ok=True); pdf_path.parent.mkdir(parents=True,exist_ok=True)
    md_path.write_text(markdown_text,encoding="utf-8")
    if args.format=="markdown":
        print(f"Built {md_path.relative_to(ROOT)}.")
        return
    css=(ROOT/"styles/icpcTemplate.css").read_text(encoding="utf-8")
    template=ROOT/"templates/document.html"
    page=render(markdown_text,cfg["title"],cfg.get("subtitle",""),cfg.get("language","zh-CN"),css,template)
    validate_html(page,markdown_text)
    if args.html_only or args.format=="html":
        html_path.write_text(page,encoding="utf-8")
        print(f"Built {md_path.relative_to(ROOT)} and {html_path.relative_to(ROOT)}.")
        return
    typ_path,toc,ast=build_typst(ROOT,cfg,markdown_text)
    if args.format=="typst":
        print(f"Built {typ_path.relative_to(ROOT)}.")
        return
    for cmd in ("pdfinfo","pdftotext"):
        if not shutil.which(cmd): raise SystemExit(f"{cmd} is required for PDF validation")
    toc_pages=compile_pdf(ROOT,cfg,typ_path,pdf_path,toc,ast)
    if set(toc_pages)!={t["id"] for t in toc}:
        raise SystemExit("PDF TOC validation failed: missing heading page numbers")
    page=render(markdown_text,cfg["title"],cfg.get("subtitle",""),cfg.get("language","zh-CN"),css,template,toc_pages=toc_pages)
    validate_html(page,markdown_text)
    html_path.write_text(page,encoding="utf-8")
    info=subprocess.run(["pdfinfo",str(pdf_path)],check=True,text=True,capture_output=True).stdout
    text=subprocess.run(["pdftotext","-layout",str(pdf_path),"-"],check=True,text=True,capture_output=True).stdout
    pages=re.search(r"^Pages:\s+(\d+)",info,re.M)
    if not pages or int(pages.group(1))<2: raise SystemExit("PDF validation failed: expected cover/contents plus chapter pages")
    size=re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts",info,re.M)
    if not size or not (590 <= float(size.group(1)) <= 600 and 836 <= float(size.group(2)) <= 847):
        raise SystemExit("PDF validation failed: page size is not A4 portrait")
    for heading in ("目录", "竞赛常用内容", "计算几何", "题意关键词索引"):
        if heading not in text: raise SystemExit(f"PDF validation failed: missing {heading}")
    page_text=text.split("\f")
    if len(page_text) < int(pages.group(1)): raise SystemExit("PDF validation failed: page text is incomplete")
    validate_pdf_bounds(pdf_path,int(pages.group(1)))
    print(f"Built {md_path.relative_to(ROOT)}, {html_path.relative_to(ROOT)}, {pdf_path.relative_to(ROOT)} ({pages.group(1)} pages).")

if __name__=="__main__": main()
