# icpcTemplate

自用 ICPC 算法板子，整理常用模板与调试方法。内容以 Markdown 管理，可构建为 Markdown、HTML 和 PDF。

## 构建

需要 Python 3.10+、Pandoc 3.1.3+，以及 Poppler 的 `pdfinfo`、`pdftotext`。PDF 使用 Typst；其编译器随 Python 依赖安装，无需 Chrome、TeXLive 或在线公式服务。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make fonts
make validate
make all
```

`make fonts` 首次从字体官方仓库下载固定版本的 Noto CJK 与 Crimson Text，并校验 SHA-256；之后可离线构建。也可以自行安装这些字体，详见 [构建说明](docs/build.md)。

PDF 按 [OI-Wiki/OI-Wiki-export](https://github.com/OI-wiki/OI-Wiki-export) 的 Typst 版式重构：A4 单栏、10 pt 宋体正文、居中小节标题、奇偶页章节页眉、9 pt 代码、语法高亮、行号和交替浅灰底。目录可点击，跨页表格重复表头，代码长行换行且跨页保持原行号。目录使用 PDF 物理页码，便于打印与电子查找。

`make markdown`、`make html`、`make typst`、`make pdf` 分别构建相应格式；`make all` 生成全部格式。主要输出为 `output/pdf/icpcTemplate.pdf`，同时生成 Markdown、内嵌样式的独立 HTML 和可独立编译的 `output/typst/icpcTemplate.typ`。HTML 提供相同视觉风格的阅读版；PDF 排版以 Typst 为准。

PDF 版式编辑 `styles/icpcTemplate.typ`，封面与目录编辑 `templates/document.typ`；HTML 样式编辑 `styles/icpcTemplate.css`。输入顺序与输出路径仍由 `config/build.json` 管理。设计来源、改动与许可见 [排版说明](docs/typesetting.md)。

## 内容格式

章节文件放在 `content/chapters/`，使用带零填充数字前缀的文件名（如 `01-...md`、`02-...md`），构建时按文件名排序。每章必须有且仅有一个一级标题 `#`。使用 `##` 作为小节标题、`cpp` 围栏代码块、标准 Markdown 表格，以及 `$...$` / `$$...$$` TeX 数学公式。关键词索引在 `config/build.json` 中单独列出，不纳入章节通配符。STL 章提供常用容器、迭代器与算法的精简速查；具体算法仍放在对应专题章，避免重复堆叠库函数清单。

`make validate` 检查章节结构、围栏代码、显式标题 ID、不可见控制字符和配置输入，不生成交付文件。也可直接运行 `python scripts/build.py --format markdown|html|typst|pdf|all`，按需使用各导出层。`make clean` 清除构建产物。

## 项目结构

```text
config/build.json             源文件顺序、标题与输出路径
content/chapters/01–09        九个编号章节
content/10-keyword-index.md   题意关键词索引
scripts/build.py             统一构建入口
scripts/typst_pdf.py          锚点兼容、公式转换与 PDF 校验
scripts/setup_fonts.py        固定版本字体下载与校验
styles/icpcTemplate.typ          Typst 正文、页眉与代码排版
styles/icpcTemplate.css          HTML 阅读样式
templates/document.typ       PDF 封面与目录
templates/document.html      独立 HTML 框架
tests/                        代码块检查与定向回归检查
docs/                         构建说明与内容覆盖表
output/                       本地生成结果与保留的样例
```

## 内容写作约定

每个算法小节都要写清适用范围、能解决什么问题，以及具体输入和输出；复杂度和边界条件应与实现一致。代码中的每个函数、构造函数、辅助函数和 lambda 都在定义前说明真实参数、返回值；`void` 函数说明修改的结构或外部状态，并标出索引约定和必要前提。不要用“输入见代码”等套话。详见 [docs/authoring.md](docs/authoring.md)。

新增内容遵循 [docs/authoring.md](docs/authoring.md)：优先归入已有章节和检查入口，保持算法源文档与版式、导出配置分层。

## 代码检查

排版构建的独立回归检查运行 `python3 tests/check_build.py`，覆盖公式转换、旧锚点、代码内容与跨页表头；不执行或修改算法代码。

在安装了 `g++` 的环境中运行：

```sh
python3 tests/check_foundations.py
python3 tests/check_algorithms.py
```

`check_foundations.py` 独立编译第 01–04 章的 C++17 围栏代码块，并运行 Python 运行/样例/三程序对拍工具的成功、失败保存、编译失败、异常退出与超时检查，以及随机结构生成器的种子复现、数组/树/图/DAG 约束检查，以及构造题断言和滑动窗口边界检查。`check_algorithms.py` 检查第 05–09 章代码块，并运行图论、数据结构、字符串和几何等算法的定向回归样例。

第 01–04 章与第 05–09 章的来源和覆盖说明见 [docs/coverage-01-04.md](docs/coverage-01-04.md) 与 [docs/coverage-05-09.md](docs/coverage-05-09.md)。
