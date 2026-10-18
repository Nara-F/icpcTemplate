PYTHON ?= python3

.PHONY: install fonts validate markdown html typst pdf all clean
install:
	$(PYTHON) -m pip install -r requirements.txt

fonts:
	$(PYTHON) scripts/setup_fonts.py

validate:
	$(PYTHON) scripts/build.py --validate-only

markdown:
	$(PYTHON) scripts/build.py --format markdown

html:
	$(PYTHON) scripts/build.py --format html

typst:
	$(PYTHON) scripts/build.py --format typst

pdf:
	$(PYTHON) scripts/build.py --format pdf

all:
	$(PYTHON) scripts/build.py --format all

clean:
	rm -f output/html/icpcTemplate.html output/markdown/icpcTemplate.md output/typst/icpcTemplate.typ output/pdf/icpcTemplate.pdf
