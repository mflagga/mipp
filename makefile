ifeq ($(OS),Windows_NT)
	RM := del /q
	RMDIR := rmdir /s /q
	MV := move
	DEVNULL := NUL 2>&1
	SLASH = $(strip \)
	PYTHON := python
else
	RM := rm -f
	RMDIR := rm -rf
	MV := mv
	DEVNULL := /dev/null
	SLASH = /
	PYTHON := python3
endif

.SUFFIXES:

LC := latexmk
STDFLAGS := -lualatex -interaction=nonstopmode
BUILDDIR := .build
TEXNAME := main
TEX = $(TEXNAME).tex
MEDIA := $(wildcard fig/*.pdf fig/ref/* fig/final/*.pdf)
REPORT := prezentacja.pdf
# nowa koncepcja (plan.txt): slajdy.tex -> slajdy.pdf (części 1–4)
SLAJDY := slajdy
# finalna prezentacja: slajdy.tex + slajdy kolegi -> prezentacja_finalna.pdf
FINAL := prezentacja_finalna
KOLEGA := src/Majorany\ w\ nanodrucie\ warunki\ i\ eksperyment.pdf

all: $(REPORT)

$(REPORT): $(TEX) $(MEDIA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(TEXNAME).pdf $@ > $(DEVNULL)

rep: $(TEX) $(MEDIA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(TEXNAME).pdf $(REPORT) > $(DEVNULL)

slajdy: $(SLAJDY).pdf

$(SLAJDY).pdf: $(SLAJDY).tex $(MEDIA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(SLAJDY).pdf $@ > $(DEVNULL)

final: $(FINAL).pdf

$(FINAL).pdf: $(FINAL).tex $(SLAJDY).tex $(MEDIA) $(KOLEGA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(FINAL).pdf $@ > $(DEVNULL)

# własne wykresy -> fig/*.pdf (wymaga numpy, scipy, matplotlib; ok. 30 s)
wykresy:
	$(PYTHON) sim/wykresy.py

clean:
	$(RM) $(REPORT) $(SLAJDY).pdf $(FINAL).pdf
# 	$(RMDIR) $(BUILDDIR)

.PHONY: all rep slajdy final wykresy clean
