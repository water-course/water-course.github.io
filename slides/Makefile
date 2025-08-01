# Makefile for compiling Quarkdown documents
# Uses quarkdown c command with -o ./dir/ --pretty --clean options

# Define the output directory
HTML_DIR = ../site/content/
PDF_DIR = ../pdf/

# List of numbered .qmd files to compile
QMD_FILES = $(wildcard *.qmd)

# Define the quarkdown command with your preferred options
QUARKDOWN_CMD = quarkdown c

# Default target
all: html

# Explicit targets for html and pdf
html: $(QMD_FILES:.qmd=.html)
pdf: $(QMD_FILES:.qmd=.pdf)

# Pattern rule to compile each .qmd file
%.html: %.qmd
	@echo "Compiling $< to $(HTML_DIR)"
	mkdir -p $(HTML_DIR)
	$(QUARKDOWN_CMD) $< -o $(HTML_DIR)

# Pattern rule to compile each .qmd file
%.pdf: %.qmd
	@echo "Compiling $< to $(PDF_DIR)"
	mkdir -p $(PDF_DIR)
	$(QUARKDOWN_CMD) $< -o $(PDF_DIR) --pdf

# Clean target to remove output files
clean:
	@echo "Cleaning output directories..."
	rm -rf $(HTML_DIR)/*
	rm -rf $(PDF_DIR)/*

# Help target
help:
	@echo "Available targets:"
	@echo "  all     - Compile all .qmd files to HTML (default)"
	@echo "  html    - Compile all .qmd files to HTML"
	@echo "  pdf     - Compile all .qmd files to PDF"
	@echo "  clean   - Remove all compiled files from output directories"
	@echo "  help    - Show this help message"
	@echo ""
	@echo "Individual files can be compiled with: make filename.html or make filename.pdf"
	@echo "Example: make 02_precipitation.html"

# Phony targets
.PHONY: all html pdf clean help
