// Adapted from OI-Wiki-export's Typst design (MIT, copyright 2020 gycy).
// Upstream: 8ab161c24bd9d3286c244f720f5c7b7a335e0dbd; see docs/typesetting.md.
#let serif-font = ("Crimson Text", "Noto Serif CJK SC")
#let sans-font = ("Crimson Text", "Noto Sans CJK SC")
#let code-font = ("DejaVu Sans Mono", "Noto Sans CJK SC")

#let running-header = context {
  let loc = here()
  let chapters = query(heading.where(level: 1))
  let current = chapters.filter(h => h.location().page() <= loc.page())
  if current.len() == 0 { return none }
  let chapter = current.last()
  let sections = query(heading.where(level: 2)).filter(h =>
    h.location().page() <= loc.page() and h.location().page() >= chapter.location().page())
  let title = if calc.odd(loc.page()) and sections.len() > 0 {
    let preceding = sections.filter(h => h.location().page() < loc.page())
    let on-page = sections.filter(h => h.location().page() == loc.page())
    let section = if on-page.len() > 0 and (preceding.len() == 0 or on-page.first().location().position().y < 25mm + 20pt) {
      on-page.first()
    } else { preceding.last() }
    [#numbering("1.1", ..counter(heading).at(section.location())) #h(.6em) #section.body]
  } else {
    [第#numbering("一", counter(heading).at(chapter.location()).first())章 #h(.6em) #chapter.body]
  }
  set text(9pt, font: serif-font)
  // Running headers must not inherit inline-code backgrounds from the body.
  show raw: it => text(font: code-font, size: 8pt, it.text)
  if calc.odd(loc.page()) { [#title #h(1fr) #counter(page).display()] }
  else { [#counter(page).display() #h(1fr) #title] }
}

#let numbered-code(it) = {
  set text(font: code-font, size: 9pt, ligatures: false, cjk-latin-spacing: none)
  set par(justify: false, leading: .45em, linebreaks: "simple")
  // Preserve syntax spans and raw line numbers through wrapping and page breaks.
  block(
    width: 100%, fill: luma(245), radius: 4pt,
    inset: (top: 4pt, bottom: 4pt), breakable: true,
    grid(
      columns: (3em, 1fr), column-gutter: .7em,
      inset: (x: 3pt, y: 2pt),
      fill: (_, y) => if calc.even(y) { none } else { white },
      ..it.lines.map(line => (
        align(right, text(fill: gray, size: 8pt, str(line.number))),
        line.body,
      )).flatten(),
    ),
  )
}

#let board-table(columns: 1, aligns: (left,), ..cells) = {
  set text(9pt)
  set par(justify: false, leading: .5em)
  table(
    columns: (1fr,) * columns,
    align: (x, _) => aligns.at(x),
    inset: 5pt, stroke: .5pt + luma(190),
    ..cells,
  )
}

#let book(body) = {
  set text(font: serif-font, size: 10pt, lang: "zh", region: "CN")
  set par(justify: true, leading: .8em, linebreaks: "optimized")
  set block(spacing: .8em)
  set heading(numbering: "1.1")
  set list(indent: 1em)
  set enum(indent: 1em)
  set strong(delta: 0)
  show strong: set text(font: sans-font, weight: 600)
  show heading: set text(font: sans-font, weight: 600)
  show heading: it => {
    let title-size = (25pt, 16pt, 14pt, 12pt, 11pt, 10pt).at(it.level - 1)
    show raw: code => text(font: sans-font, size: title-size, code.text)
    context metadata((id: str(it.label).trim("<", at: start).trim(">", at: end), page: it.location().page()))
    it
  }
  show heading.where(level: 1): it => {
    context metadata((id: str(it.label).trim("<", at: start).trim(">", at: end), page: it.location().page()))
    pagebreak(weak: true)
    block(above: 10mm, below: 10mm)[
      #text(25pt, font: serif-font, weight: 700)[
        #context [第#counter(heading).display("一")章]
        #v(3mm)
        #it.body
      ]
    ]
  }
  show heading.where(level: 2): it => {
    set text(16pt)
    block(width: 100%, above: 1.3em, below: 1em, sticky: true, align(center, it))
  }
  show heading.where(level: 3): set text(14pt)
  show math.equation: set text(font: "New Computer Modern Math")
  show raw: set text(font: code-font, size: 9pt, ligatures: false)
  show raw.where(block: false): it => highlight(fill: luma(95%), it)
  show raw.where(block: true): numbered-code
  show table.cell.where(y: 0): set text(font: sans-font, weight: 600)
  show quote.where(block: true): it => block(stroke: (left: 2pt + luma(80%)), inset: (left: 1em), it.body)
  body
}
