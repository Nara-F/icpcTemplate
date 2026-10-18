"""Pandoc AST -> Typst, preserving the existing Markdown/HTML anchors."""
from __future__ import annotations

import json
import re
import shutil
import subprocess


def pandoc(*args, source):
    executable = shutil.which("pandoc")
    if not executable:
        raise SystemExit("Pandoc >= 3.1.3 is required for PDF/Typst output.")
    result = subprocess.run(
        [executable, *args, "--fail-if-warnings"], input=source,
        text=True, capture_output=True,
    )
    if result.returncode:
        raise SystemExit("Pandoc conversion failed:\n" + result.stderr)
    return result.stdout


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def flatten_toc(tokens):
    for token in tokens:
        yield token
        yield from flatten_toc(token.get("children", []))


def build_typst(root, cfg, markdown_text):
    import markdown

    # Use the old renderer's IDs, including explicit IDs and duplicate suffixes.
    # Pandoc's automatic IDs differ for Chinese and numbered headings.
    md = markdown.Markdown(extensions=["extra", "toc"],
                           extension_configs={"toc": {"toc_depth": "1-6"}})
    md.convert(markdown_text)
    toc = list(flatten_toc(md.toc_tokens))
    ast = json.loads(pandoc(
        "--from=markdown+tex_math_dollars-smart", "--to=json", source=markdown_text,
    ))
    headers = [node for node in walk(ast) if node.get("t") == "Header"]
    if len(headers) != len(toc):
        raise SystemExit("Markdown/Pandoc heading counts differ; refusing to change anchors.")
    for node, token in zip(headers, toc):
        level, attr, inlines = node["c"]
        if level != token["level"]:
            raise SystemExit("Markdown/Pandoc heading levels differ.")
        attr[0] = token["id"]
        # Sources already contain 1. / 1.1 etc.; Typst owns visible numbering.
        if inlines and inlines[0]["t"] == "Str" and re.fullmatch(r"\d+(?:\.\d+)*\.?", inlines[0]["c"]):
            inlines.pop(0)
            if inlines and inlines[0]["t"] == "Space":
                inlines.pop(0)
    ids = {token["id"] for token in toc}
    for node in walk(ast):
        if node.get("t") == "Link":
            target = node["c"][2][0]
            if target.startswith("#") and target[1:] not in ids:
                raise SystemExit(f"Broken PDF link: {target}")

    # TeX consumes one unbraced character after ^/_. Make this explicit before
    # texmath conversion: e.g. n^22^n is n^{2}2^{n}, not n^{22^n}.
    for node in walk(ast):
        if node.get("t") == "Math":
            node["c"][1] = re.sub(r"(?<!\\)([\^_])([A-Za-z0-9])", r"\1{\2}", node["c"][1])

    # Raw blocks are passed through the writer, including every original code
    # line and its indentation. Fail on conversion warnings (including TeX).
    body = pandoc("--from=json", "--to=typst", "--wrap=none",
                  "--lua-filter=" + str(root / "scripts/typst-tables.lua"),
                  source=json.dumps(ast, ensure_ascii=False))
    out = root / cfg["typst"]
    out.parent.mkdir(parents=True, exist_ok=True)
    # Generated .typ is self-contained and can also be compiled with Typst CLI.
    template = (root / "templates/document.typ").read_text(encoding="utf-8")
    style = (root / "styles/icpcTemplate.typ").read_text(encoding="utf-8")
    for key in ("title", "subtitle"):
        template = template.replace("{{ " + key + " }}", json.dumps(cfg.get(key, ""), ensure_ascii=False))
    out.write_text(style + "\n" + template + "\n" + body, encoding="utf-8")
    return out, toc, ast


def compile_pdf(root, cfg, typ_path, pdf_path, toc, ast):
    try:
        import typst
    except ImportError as exc:
        raise SystemExit("Typst binding missing. Run: python3 -m pip install -r requirements.txt") from exc
    font_paths = [str(root / p) for p in cfg.get("font_paths", [".fonts"])]
    compiler = typst.Compiler(str(typ_path), root=str(root), font_paths=font_paths)
    try:
        pdf_bytes, warnings = compiler.compile_with_warnings()
        if warnings:
            raise SystemExit("Typst warnings (check fonts and layout):\n" + "\n".join(map(str, warnings)))
        # Check the actual document tree, not just generated source text.
        raw = json.loads(compiler.query("raw.where(block: true)", field="text"))
        code = [n["c"][1] for n in walk(ast) if n.get("t") == "CodeBlock"]
        if raw != code:
            raise SystemExit("PDF code preservation failed: rendered raw blocks differ from sources.")
        actual_ids = json.loads(compiler.query("heading", field="label"))
        if actual_ids != ["<" + t["id"] + ">" for t in toc]:
            raise SystemExit("PDF heading preservation failed: labels differ from sources.")
        # The style emits physical page metadata at each heading. Use it to
        # populate the HTML TOC with the same printed PDF page numbers.
        entries = json.loads(compiler.query("metadata", field="value"))
        pages = {e["id"]: e["page"] for e in entries if isinstance(e, dict) and "id" in e}
        if set(pages) != {t["id"] for t in toc}:
            raise SystemExit("PDF TOC validation failed: missing heading page numbers")
        pdf_path.write_bytes(pdf_bytes)
        return pages
    except typst.TypstError as exc:
        raise SystemExit(str(exc)) from exc
