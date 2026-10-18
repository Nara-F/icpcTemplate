# OI-Wiki 风格排版

本次排版参考 [OI-wiki/OI-Wiki-export](https://github.com/OI-wiki/OI-Wiki-export) 的 Typst 版，基准提交 `8ab161c24bd9d3286c244f720f5c7b7a335e0dbd`。主要参考文件是 `oi-wiki-export-typst/oi-wiki-export.typ`、`oi-wiki.typ` 与 `constants.typ`。改编的排版代码保留其 MIT 许可，完整许可见 [OI-Wiki-export-LICENSE](OI-Wiki-export-LICENSE)。该声明只涉及排版参考代码，不改变本仓库算法内容的许可。

| 版式 | 实现 |
|---|---|
| 页面 | A4 纵向单栏，左右 25 mm、上 25 mm、下 24 mm 页边距 |
| 正文 | 10 pt Crimson Text + Noto Serif CJK SC，两端对齐 |
| 标题 | 章节中文编号与 25 pt 宋体章名；16 pt 居中小节标题 |
| 页眉 | 偶数页章名，奇数页小节名，页码位于外侧 |
| 代码 | 9 pt DejaVu Sans Mono + Noto Sans CJK SC，行号、彩色语法、浅灰/白交替行底色 |
| 公式 | 原生数学排版，独立公式居中 |
| 表格 | 9 pt、浅灰细边框、续页重复表头 |
| 导航 | 二级可点击目录、PDF 书签、原有关键词索引锚点 |

面向竞赛手册作了少量调整：章标题与正文共页；不额外插入空白偶数页或背封；封面与目录使用连续物理页码。保留 `icpcTemplate` 标题和 Nara-F 署名，未使用 OI Wiki 的标志或署名。字体下载版本和校验值见 `config/fonts.json`，字体许可随 `make fonts` 一并保存。

PDF 样式与 HTML 阅读样式分开维护，算法源文件保持原样。HTML 单独导出时不显示 PDF 页码；完整构建后其目录页码来自同一次 PDF 排版。
