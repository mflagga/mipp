ifeq ($(OS),Windows_NT)
	RM := del /q
	RMDIR := rmdir /s /q
	MV := move
	DEVNULL := NUL 2>&1
	SLASH = $(strip \)
else
	RM := rm -f
	RMDIR := rm -rf
	MV := mv
	DEVNULL := /dev/null
	SLASH = /
endif

.SUFFIXES:

LC := latexmk
STDFLAGS := -lualatex -interaction=nonstopmode
BUILDDIR := .build
TEXNAME := main
TEX = $(TEXNAME).tex
MEDIA := $(wildcard fig/*.pdf fig/ref/*.png)
REPORT := prezentacja.pdf

all: $(REPORT)

$(REPORT): $(TEX) $(MEDIA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(TEXNAME).pdf $@ > $(DEVNULL)

rep: $(TEX) $(MEDIA)
	$(LC) $(STDFLAGS) -output-directory=$(BUILDDIR) $< > $(DEVNULL)
	$(MV) $(BUILDDIR)$(SLASH)$(TEXNAME).pdf $(REPORT) > $(DEVNULL)

clean:
	$(RM) $(REPORT)
# 	$(RMDIR) $(BUILDDIR)

.PHONY: all rep clean
