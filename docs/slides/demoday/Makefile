#
# Makefile for The Onion Plan slides
# Inspired by https://gitlab.torproject.org/anarcat/presentations/-/blob/main/soto-2022/Makefile
#

TARGET				  = demoday.pdf
TEMPLATE        = beamer-ahf-slim.tex
TEMPLATE_FOLDER = ../../../vendors/onion-tex-slim/src/pandoc/templates/$(TEMPLATE)
COMPILE_CMD     = pandoc -t beamer --pdf-engine=pdflatex --slide-level 2 --template="$(TEMPLATE_FOLDER)"

export TEXINPUTS:=$(shell pwd)/../../../vendors/onion-tex-slim/src/tex:${TEXINPUTS}

all: $(TARGET)

%.pdf: %.md
	@$(COMPILE_CMD) $< -o $@

clean:
	@rm *.pdf || true
