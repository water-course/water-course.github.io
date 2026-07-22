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

# Define the quarkdown command with your preferred options.
# --strict makes Quarkdown exit non-zero on hard errors.
# --allow=global-read grants read access outside each document's own directory.
# The category subdirectories (lectures/, tutorials/, ...) include shared files
# from the slides root via "../" (definitions*.qd, image/, ...). Quarkdown's
# sandbox denies those escaping reads by default, so without this the decks
# render "not enough privileges" error boxes instead of the real content.
QUARKDOWN_CMD = quarkdown c --strict --allow=global-read

# Compile one document and treat ANY problem as fatal. Quarkdown does not exit
# non-zero for soft problems -- an unresolvable image or a denied file access
# only prints a warning line and still returns success -- so we capture its
# output and fail the build if the exit code is non-zero or the output contains
# any known problem signature. This guarantees a broken slide breaks compilation
# instead of shipping silently.
FATAL_PATTERN = \[!\]|not enough privileges|Cannot access file|Unresolved|[Ee]rror:
define compile
	@echo "Compiling $< to $(1)"
	@mkdir -p $(1)
	@out=$$($(QUARKDOWN_CMD) $< -o $(1) $(2) 2>&1); rc=$$?; \
	 printf '%s\n' "$$out" | sed $$'s/\x1b\\[[0-9;]*m//g'; \
	 if [ $$rc -ne 0 ] || printf '%s' "$$out" | grep -qE '$(FATAL_PATTERN)'; then \
	   echo ">>> BUILD FAILED: Quarkdown reported a problem in $< (see above)"; \
	   exit 1; \
	 fi
endef

# Default target
all: html

# Explicit targets for html and pdf
html: $(QMD_FILES:.qd=.html)
pdf: $(QMD_FILES:.qd=.pdf)

# Pattern rule to compile each .qd file
%.html: %.qd
	$(call compile,$(HTML_DIR),)

# Pattern rule to compile each .qd file
%.pdf: %.qd
	$(call compile,$(PDF_DIR),--pdf)

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
