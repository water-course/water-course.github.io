# Makefile for compiling Quarkdown documents
# Uses quarkdown c command with -o ./dir/ options
#
# Source .qd files live in category subdirectories (lectures/, tutorials/,
# assignments/, overviews/, exams/). The shared includes (definitions.qd,
# definitions_slides.qd) sit at this root and are pulled in via .include, so
# they must NOT be compiled as standalone documents.

# Define the output directory
HTML_DIR = ../site/content/
PDF_DIR = ../pdf/

# All standalone Quarkdown documents, found recursively in the category
# subdirectories. definitions*.qd are includes, not documents, so they are
# excluded (they have no docname and would produce junk output).
QMD_FILES = $(shell find . -name '*.qd' -not -name 'definitions*.qd')

# Define the quarkdown command with your preferred options
QUARKDOWN_CMD = quarkdown c

# Default target
all: html

# Explicit targets for html and pdf
html: $(QMD_FILES:.qd=.html)
pdf: $(QMD_FILES:.qd=.pdf)

# Pattern rule to compile each .qd file
%.html: %.qd
	@echo "Compiling $< to $(HTML_DIR)"
	mkdir -p $(HTML_DIR)
	$(QUARKDOWN_CMD) $< -o $(HTML_DIR)

# Pattern rule to compile each .qd file
%.pdf: %.qd
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
	@echo "  all     - Compile all .qd files to HTML (default)"
	@echo "  html    - Compile all .qd files to HTML"
	@echo "  pdf     - Compile all .qd files to PDF"
	@echo "  clean   - Remove all compiled files from output directories"
	@echo "  help    - Show this help message"
	@echo ""
	@echo "Individual files can be compiled with: make path/to/filename.html"
	@echo "Example: make lectures/precipitation.html"

# Phony targets
.PHONY: all html pdf clean help
