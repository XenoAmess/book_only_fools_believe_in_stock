#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert markdown files from src/part0-src/part6 to PDF format
"""

import os
import glob
import subprocess
from pathlib import Path

def convert_md_to_pdf_wkhtmltopdf(md_file, pdf_file):
    """Convert markdown to PDF using wkhtmltopdf via pandoc"""
    try:
        # Use pandoc to convert markdown to HTML first, then to PDF
        cmd = [
            'pandoc',
            md_file,
            '-o', pdf_file,
            '--pdf-engine=wkhtmltopdf',
            '--css=pdf_style.css',
            '--toc',
            '--toc-depth=3',
            '--variable', 'geometry:margin=1in',
            '--variable', 'fontsize=12pt',
            '--variable', 'documentclass=article',
            '--variable', 'mainfont=SimSun',
            '--variable', 'CJKmainfont=SimSun'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✓ Converted {md_file} to {pdf_file}")
            return True
        else:
            print(f"✗ Failed to convert {md_file}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error converting {md_file}: {e}")
        return False

def convert_md_to_pdf_basic(md_file, pdf_file):
    """Fallback method using pandoc with basic PDF output"""
    try:
        cmd = [
            'pandoc',
            md_file,
            '-o', pdf_file,
            '--toc',
            '--toc-depth=3',
            '--variable', 'geometry:margin=1in',
            '--variable', 'fontsize=12pt'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✓ Converted {md_file} to {pdf_file} (basic method)")
            return True
        else:
            print(f"✗ Failed to convert {md_file}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error converting {md_file}: {e}")
        return False

def create_css_style():
    """Create CSS style for better PDF formatting"""
    css_content = """
body {
    font-family: "SimSun", "Microsoft YaHei", "WenQuanYi Micro Hei", serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "SimSun", "Microsoft YaHei", "WenQuanYi Micro Hei", serif;
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: bold;
}

h1 {
    font-size: 18pt;
    border-bottom: 2px solid #34495e;
    padding-bottom: 0.3em;
}

h2 {
    font-size: 16pt;
    color: #34495e;
}

h3 {
    font-size: 14pt;
    color: #7f8c8d;
}

p {
    text-align: justify;
    margin-bottom: 1em;
    text-indent: 2em;
}

blockquote {
    border-left: 4px solid #bdc3c7;
    padding-left: 1em;
    margin-left: 0;
    font-style: italic;
    color: #7f8c8d;
}

code {
    background-color: #f8f9fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: "Courier New", monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f8f9fa;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    border: 1px solid #e9ecef;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.75em;
    text-align: left;
}

th {
    background-color: #f8f9fa;
    font-weight: bold;
}

@media print {
    body {
        font-size: 11pt;
    }

    h1 {
        page-break-before: always;
    }

    h1:first-of-type {
        page-break-before: auto;
    }
}
"""

    with open('pdf_style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✓ Created CSS style file")

def main():
    """Main conversion function"""
    print("=== Markdown to PDF Converter ===")
    print("Converting content from src/part0-src/part6 to PDF format")

    # Create CSS style file
    create_css_style()

    # Create output directory
    output_dir = "pdf_output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Created output directory: {output_dir}")

    # Get all markdown files
    all_files = []
    for i in range(7):  # part0 to part6
        pattern = f"src/part{i}/*.md"
        files = glob.glob(pattern)
        all_files.extend(files)

    # Sort files by part number and then by filename
    all_files.sort(key=lambda x: (int(x.split('/part')[1].split('/')[0]), x))

    print(f"Found {len(all_files)} markdown files to convert:")
    for file in all_files:
        print(f"  - {file}")

    # Convert each file
    success_count = 0
    total_count = len(all_files)

    for md_file in all_files:
        # Generate output filename
        base_name = os.path.basename(md_file).replace('.md', '.pdf')
        pdf_file = os.path.join(output_dir, base_name)

        print(f"\nConverting: {md_file}")

        # Try wkhtmltopdf method first
        success = convert_md_to_pdf_wkhtmltopdf(md_file, pdf_file)

        # If that fails, try basic pandoc method
        if not success:
            print("Trying basic pandoc method...")
            success = convert_md_to_pdf_basic(md_file, pdf_file)

        if success:
            success_count += 1

    print(f"\n=== Conversion Complete ===")
    print(f"Successfully converted: {success_count}/{total_count} files")
    print(f"Output directory: {output_dir}")

    # Also create a combined PDF if possible
    if success_count > 0:
        print("\nAttempting to create combined PDF...")
        combined_pdf = os.path.join(output_dir, "combined_all_parts.pdf")

        # Try to combine all PDFs
        try:
            from PyPDF2 import PdfMerger
            merger = PdfMerger()

            pdf_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir)
                        if f.endswith('.pdf') and f != 'combined_all_parts.pdf']
            pdf_files.sort()

            for pdf_file in pdf_files:
                merger.append(pdf_file)

            merger.write(combined_pdf)
            merger.close()
            print(f"✓ Created combined PDF: {combined_pdf}")
        except ImportError:
            print("PyPDF2 not available, skipping combined PDF creation")
        except Exception as e:
            print(f"Could not create combined PDF: {e}")

if __name__ == "__main__":
    main()