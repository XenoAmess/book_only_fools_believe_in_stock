#!/bin/bash

# Script to create PDFs from HTML files

echo "=== Creating PDFs from HTML ==="

# Create pdf_output directory
mkdir -p pdf_output

# Function to convert HTML to PDF using available tools
convert_html_to_pdf() {
    local html_file="$1"
    local pdf_file="$2"

    echo "Converting $html_file to PDF..."

    # Try using wkhtmltopdf if available
    if command -v wkhtmltopdf >/dev/null 2>&1; then
        echo "Using wkhtmltopdf..."
        wkhtmltopdf --enable-local-file-access \
                   --print-media-type \
                   --page-size A4 \
                   --margin-top 2cm \
                   --margin-bottom 2cm \
                   --margin-left 1.5cm \
                   --margin-right 1.5cm \
                   --encoding UTF-8 \
                   "$html_file" "$pdf_file"
        return $?
    fi

    # Try using weasyprint if available
    if command -v weasyprint >/dev/null 2>&1; then
        echo "Using weasyprint..."
        weasyprint "$html_file" "$pdf_file"
        return $?
    fi

    # Try using pandoc with HTML input
    if command -v pandoc >/dev/null 2>&1; then
        echo "Using pandoc..."
        pandoc "$html_file" -o "$pdf_file" --pdf-engine=wkhtmltopdf
        return $?
    fi

    echo "No suitable PDF converter found. Please install one of:"
    echo "- wkhtmltopdf: sudo apt install wkhtmltopdf"
    echo "- weasyprint: pip install weasyprint"
    echo "- Or use browser print: Open HTML in Chrome/Firefox and print to PDF"
    return 1
}

# Convert individual HTML files
echo "Converting individual HTML files to PDF..."
success_count=0

for html_file in html_output/part*/*.html; do
    if [ -f "$html_file" ]; then
        base_name=$(basename "$html_file" .html)
        pdf_file="pdf_output/${base_name}.pdf"

        if convert_html_to_pdf "$html_file" "$pdf_file"; then
            success_count=$((success_count + 1))
        fi
    fi
done

# Convert combined HTML file
if [ -f "html_output/combined_all_parts.html" ]; then
    echo ""
    echo "Converting combined HTML file..."
    convert_html_to_pdf "html_output/combined_all_parts.html" "pdf_output/combined_all_parts.pdf"
fi

echo ""
echo "=== PDF Creation Complete ==="
echo "Successfully created $success_count individual PDFs"
echo "PDF files are available in: pdf_output/"
echo ""
echo "Alternative method if PDF conversion failed:"
echo "1. Open html_output/combined_all_parts.html in your browser"
echo "2. Press Ctrl+P (or Cmd+P on Mac)"
echo "3. Select 'Save as PDF' as destination"
echo "4. Choose appropriate settings and save"
echo ""
echo "The HTML files are print-ready with proper styling for PDF conversion."