#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert markdown files from src/part0-src/part6 to PDF format using HTML intermediate
"""

import os
import glob
import subprocess
import markdown
from pathlib import Path
from markdown.extensions import codehilite, tables, toc

def create_html_template():
    """Create HTML template with proper Chinese character support"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {
            size: A4;
            margin: 2cm 1.5cm;
        }

        body {
            font-family: "Times New Roman", "SimSun", "Microsoft YaHei", "WenQuanYi Micro Hei", serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: justify;
        }

        .container {
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: "Times New Roman", "SimSun", "Microsoft YaHei", serif;
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 1em;
            font-weight: bold;
            page-break-after: avoid;
        }

        h1 {
            font-size: 18pt;
            color: #c0392b;
            border-bottom: 3px solid #e74c3c;
            padding-bottom: 0.5em;
            text-align: center;
            margin-top: 1em;
        }

        h2 {
            font-size: 16pt;
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 1em;
            background-color: #f8f9fa;
            padding-top: 0.5em;
            padding-bottom: 0.5em;
        }

        h3 {
            font-size: 14pt;
            color: #7f8c8d;
            font-style: italic;
        }

        h4 {
            font-size: 13pt;
            color: #95a5a6;
        }

        p {
            margin-bottom: 1.2em;
            text-indent: 2em;
            orphans: 2;
            widows: 2;
        }

        blockquote {
            border-left: 4px solid #bdc3c7;
            padding-left: 1.5em;
            margin-left: 0;
            margin-right: 0;
            font-style: italic;
            color: #7f8c8d;
            background-color: #f8f9fa;
            padding-top: 0.5em;
            padding-bottom: 0.5em;
        }

        code {
            background-color: #f8f9fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
            border: 1px solid #e9ecef;
        }

        pre {
            background-color: #f8f9fa;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #e9ecef;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }

        pre code {
            background: none;
            padding: 0;
            border: none;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 11pt;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 0.75em;
            text-align: left;
        }

        th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }

        ul, ol {
            margin-bottom: 1em;
            padding-left: 2em;
        }

        li {
            margin-bottom: 0.5em;
        }

        .toc {
            page-break-after: always;
            background-color: #f8f9fa;
            padding: 2em;
            border-radius: 10px;
            margin-bottom: 2em;
        }

        .toc h2 {
            color: #c0392b;
            border: none;
            background: none;
            padding: 0;
            text-align: center;
            margin-bottom: 1.5em;
        }

        .toc ul {
            list-style: none;
            padding-left: 0;
        }

        .toc li {
            margin-bottom: 0.8em;
            padding-left: 1em;
        }

        .toc a {
            color: #3498db;
            text-decoration: none;
        }

        .toc a:hover {
            text-decoration: underline;
        }

        strong {
            color: #c0392b;
            font-weight: bold;
        }

        em {
            color: #8e44ad;
            font-style: italic;
        }

        .page-break {
            page-break-before: always;
        }

        @media print {
            body {
                font-size: 11pt;
                line-height: 1.6;
            }

            h1 {
                page-break-before: always;
                font-size: 16pt;
            }

            h1:first-of-type {
                page-break-before: auto;
            }

            h2 {
                font-size: 14pt;
            }

            h3 {
                font-size: 12pt;
            }

            p {
                text-indent: 2em;
                orphans: 2;
                widows: 2;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""

def convert_md_to_html(md_file):
    """Convert markdown to HTML with proper extensions"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Configure markdown extensions
        md = markdown.Markdown(extensions=[
            'codehilite',
            'tables',
            'toc',
            'fenced_code',
            'nl2br',
            'smarty'
        ])

        html_content = md.convert(md_content)

        # Get title from first heading or filename
        title = os.path.basename(md_file).replace('.md', '').replace('_', ' ')

        # Create full HTML
        template = create_html_template()
        full_html = template.format(title=title, content=html_content)

        # Save HTML file
        html_file = md_file.replace('.md', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"✓ Converted {md_file} to HTML")
        return html_file
    except Exception as e:
        print(f"✗ Error converting {md_file} to HTML: {e}")
        return None

def convert_html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF using wkhtmltopdf or weasyprint"""
    try:
        # Try wkhtmltopdf first
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--print-media-type',
            '--page-size', 'A4',
            '--margin-top', '2cm',
            '--margin-bottom', '2cm',
            '--margin-left', '1.5cm',
            '--margin-right', '1.5cm',
            '--encoding', 'UTF-8',
            '--minimum-font-size', '12',
            html_file,
            pdf_file
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print(f"✓ Converted {html_file} to PDF using wkhtmltopdf")
            return True
        else:
            print(f"wkhtmltopdf failed, trying weasyprint...")

            # Try weasyprint as fallback
            cmd = ['weasyprint', html_file, pdf_file]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                print(f"✓ Converted {html_file} to PDF using weasyprint")
                return True
            else:
                print(f"✗ Both PDF engines failed: {result.stderr}")
                return False

    except FileNotFoundError:
        print("Neither wkhtmltopdf nor weasyprint found. Installing weasyprint...")
        return False
    except Exception as e:
        print(f"✗ Error converting HTML to PDF: {e}")
        return False

def install_requirements():
    """Install required packages"""
    packages = [
        'markdown',
        'weasyprint',
        'PyPDF2'
    ]

    for package in packages:
        try:
            subprocess.run(['pip3', 'install', package], check=True)
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def main():
    """Main conversion function"""
    print("=== Markdown to PDF Converter (HTML Method) ===")
    print("Converting content from src/part0-src/part6 to PDF format")

    # Install requirements first
    print("Installing required packages...")
    install_requirements()

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
    html_files = []

    # First, convert all markdown to HTML
    print("\n=== Converting Markdown to HTML ===")
    for md_file in all_files:
        html_file = convert_md_to_html(md_file)
        if html_file:
            html_files.append(html_file)

    print(f"\n=== Converting HTML to PDF ===")
    for html_file in html_files:
        # Generate output filename
        base_name = os.path.basename(html_file).replace('.html', '.pdf')
        pdf_file = os.path.join(output_dir, base_name)

        print(f"\nConverting: {html_file}")

        # Convert HTML to PDF
        success = convert_html_to_pdf(html_file, pdf_file)

        if success:
            success_count += 1
            # Clean up HTML file
            try:
                os.remove(html_file)
            except:
                pass

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