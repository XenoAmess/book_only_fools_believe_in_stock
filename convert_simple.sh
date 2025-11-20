#!/bin/bash

# Simple script to convert markdown files to PDF using pandoc with Chinese support

echo "=== Converting Markdown to PDF ==="

# Create output directory
mkdir -p pdf_output

# Install required packages if not available
echo "Installing required packages..."
sudo apt update
sudo apt install -y pandoc texlive-xetex texlive-lang-chinese fonts-noto-cjk

# Create a simple LaTeX template for Chinese support
cat > chinese_template.latex << 'EOF'
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{xcolor}

% Set Chinese fonts
\setCJKmainfont{Noto Serif CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}

% Page setup
\geometry{a4paper, margin=2.5cm}
\onehalfspacing
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[LO,RE]{\leftmark}
\renewcommand{\headrulewidth}{0.4pt}

% Colors
\definecolor{titlecolor}{RGB}{44, 62, 80}
\definecolor{subtitlecolor}{RGB}{52, 73, 94}

% Section formatting
\usepackage{titlesec}
\titleformat{\section}[block]{\Large\bfseries\color{titlecolor}}{\thesection}{1em}{}
\titleformat{\subsection}[block]{\large\bfseries\color{subtitlecolor}}{\thesubsection}{1em}{}

% Table of contents
\usepackage{tocloft}
\renewcommand{\cfttoctitlefont}{\hfill\Large\bfseries}
\renewcommand{\cftaftertoctitle}{\hfill}

\begin{document}

$body$

\end{document}
EOF

# Function to convert single file
convert_file() {
    local md_file="$1"
    local base_name=$(basename "$md_file" .md)
    local pdf_file="pdf_output/${base_name}.pdf"

    echo "Converting: $md_file"

    # Convert using pandoc with our template
    pandoc "$md_file" \
        --pdf-engine=xelatex \
        --template=chinese_template.latex \
        --toc \
        --toc-depth=3 \
        -o "$pdf_file"

    if [ $? -eq 0 ]; then
        echo "✓ Successfully converted to $pdf_file"
        return 0
    else
        echo "✗ Failed to convert $md_file"
        return 1
    fi
}

# Convert all markdown files
success_count=0
total_count=0

for part in {0..6}; do
    if [ -d "src/part$part" ]; then
        for md_file in src/part$part/*.md; do
            if [ -f "$md_file" ]; then
                total_count=$((total_count + 1))
                if convert_file "$md_file"; then
                    success_count=$((success_count + 1))
                fi
            fi
        done
    fi
done

echo ""
echo "=== Conversion Complete ==="
echo "Successfully converted: $success_count/$total_count files"
echo "Output directory: pdf_output"

# Try to create combined PDF if we have successful conversions
if [ $success_count -gt 0 ]; then
    echo ""
    echo "Creating combined PDF..."

    # Install pdfunite if available
    sudo apt install -y poppler-utils

    # Get all PDF files in order
    pdf_files=()
    for part in {0..6}; do
        for pdf in pdf_output/part_${part}_*.pdf; do
            if [ -f "$pdf" ]; then
                pdf_files+=("$pdf")
            fi
        done
    done

    if [ ${#pdf_files[@]} -gt 0 ]; then
        pdfunite "${pdf_files[@]}" pdf_output/combined_all_parts.pdf
        if [ $? -eq 0 ]; then
            echo "✓ Created combined PDF: pdf_output/combined_all_parts.pdf"
        else
            echo "✗ Failed to create combined PDF"
        fi
    fi
fi

# Clean up template file
rm -f chinese_template.latex

echo ""
echo "All done! Check the pdf_output directory for your PDF files."