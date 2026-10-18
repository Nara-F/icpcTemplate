# 构建与导出

## 依赖

- Python 3.10+：`python3 -m pip install -r requirements.txt`。
- Pandoc 3.1.3+：必须支持 `typst` 输出；Debian/Ubuntu 较旧的软件源可能需要从 Pandoc 官方 release 安装。
- Poppler：`pdfinfo`、`pdftotext` 用于检查页面尺寸、文字和边界。
- 字体：运行 `make fonts` 下载 `config/fonts.json` 固定的 Noto Serif CJK SC、Noto Sans CJK SC、Crimson Text 及其 OFL 许可；约 100 MB，保存在忽略提交的 `.fonts/`。下载校验 SHA-256，已有正确文件会复用。DejaVu Sans Mono、New Computer Modern Math 随 Typst 提供。

`requirements.txt` 固定 Typst Python binding 为 0.15.0，自带编译器。不需要 Chrome、Node、TeXLive 或 Typst Universe 包下载。第一次准备依赖与字体后，所有构建均可离线运行。若自行安装字体，确保字体家族名称一致；`config/build.json` 的 `font_paths` 可添加本地字体目录。缺字或未知字体警告会阻止 PDF 发布。

## 命令

```sh
make fonts
make validate
make all
python3 tests/check_build.py
```

`make validate` 仅检查源文件。`make markdown` 组装 Markdown；`make html` 导出 Markdown 和 HTML；`make typst` 导出 Markdown 与自包含 Typst 源；`make pdf` / `make all` 生成四种格式。直接调用时可用 `python scripts/build.py --format markdown|html|typst|pdf|all`。旧的 `--html-only` 仍可用。

| 文件 | 用途 |
|---|---|
| `output/markdown/icpcTemplate.md` | 合并后的源文本 |
| `output/html/icpcTemplate.html` | 内嵌 CSS 的独立阅读版，完整构建后目录列出 PDF 页码 |
| `output/typst/icpcTemplate.typ` | 自包含 Typst 文件，`typst compile --font-path .fonts` 也可编译 |
| `output/pdf/icpcTemplate.pdf` | 可打印 PDF，作为仓库中的成品样例保留 |

`make clean` 删除以上生成结果；不会删除源文档或缓存字体。

## 构建过程与检查

Python Markdown 继续负责 HTML 与现有标题 ID。PDF 使用 Pandoc 的结构化 AST，保留这些 ID，避免关键词索引的旧链接失效；仅在导出时去除手写标题编号，交给 Typst 统一编号。原始 Markdown 与代码无需迁移。

TeX 公式由 Pandoc 转为原生 Typst 数学；转换前显式补齐单字符上下标的花括号，避免 `n^22^n` 被误读为嵌套指数。转换警告会终止构建。表格通过一个小型 Lua 过滤器生成原生 `table.header`，在续页重复表头。

构建会比对原始代码块与 Typst 实际文档树中的代码文本、检查所有标题 ID 和内部链接，并检查 PDF 的 A4 尺寸、章节文字、页数和页面边界。Typst 自己计算目录页码；同一份物理页码会写回 HTML 目录。PDF 自带书签，页码连续包含封面与目录。

内容改动仍按 `docs/authoring.md` 运行相应算法检查。排版变化运行 `tests/check_build.py`、`make validate`、`make all`，并渲染目录、长代码、公式与跨页表格页面检查。
