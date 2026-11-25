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
MEDIA := $(wildcard fig/*.pdf fig/ref/*)
REPORT := prezentacja.pdf
# nowa koncepcja (plan.txt): slajdy.tex -> slajdy.pdf
SLAJDY := slajdy

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

# własne wykresy -> fig/*.pdf (wymaga numpy, scipy, matplotlib; ok. 30 s)
wykresy:
	$(PYTHON) sim/wykresy.py

clean:
	$(RM) $(REPORT) $(SLAJDY).pdf
# 	$(RMDIR) $(BUILDDIR)

.PHONY: all rep slajdy wykresy clean
