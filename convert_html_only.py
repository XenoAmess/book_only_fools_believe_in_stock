#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert markdown files to HTML format with proper styling for easy PDF conversion
"""

import os
import glob
import re
from pathlib import Path

def create_html_template():
    """Create HTML template with proper Chinese character support and print-friendly CSS"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @media print {
            @page {
                size: A4;
                margin: 2cm 1.5cm;
            }

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

        body {
            font-family: "Times New Roman", "SimSun", "Microsoft YaHei", "WenQuanYi Micro Hei", serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            text-align: justify;
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
    </style>
</head>
<body>
    {content}
</body>
</html>"""

def simple_markdown_to_html(md_content):
    """Simple markdown to HTML conversion"""
    html = md_content

    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

    # Code blocks
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)

    # Blockquotes
    html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Line breaks and paragraphs
    paragraphs = html.split('\n\n')
    html_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if para:
            # Skip if it's already a block element
            if not (para.startswith('<h') or para.startswith('<block') or para.startswith('<pre') or para.startswith('<ul') or para.startswith('<ol')):
                para = f'<p>{para}</p>'
            html_paragraphs.append(para)

    return '\n'.join(html_paragraphs)

def convert_md_file_to_html(md_file):
    """Convert a single markdown file to HTML"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = simple_markdown_to_html(md_content)

        # Get title from filename
        title = os.path.basename(md_file).replace('.md', '').replace('_', ' ')

        # Create full HTML
        template = create_html_template()
        full_html = template.format(content=html_content, title=title)

        # Save HTML file
        html_file = md_file.replace('.md', '.html')
        html_file = html_file.replace('src/', 'html_output/')

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(html_file), exist_ok=True)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"✓ Converted {md_file} to {html_file}")
        return html_file
    except Exception as e:
        print(f"✗ Error converting {md_file}: {e}")
        return None

def create_combined_html():
    """Create a combined HTML file with all parts"""
    combined_content = []

    # Add title page
    title_page = """
    <h1>《只有弱智才买股票》</h1>
    <div style="text-align: center; margin-top: 3em;">
        <h2>二级市场与生产实践的彻底脱节</h2>
        <h3>——一个投机泡沫的悼词</h3>
    </div>
    <div style="page-break-after: always;"></div>
    """
    combined_content.append(title_page)

    # Add table of contents
    toc = """
    <div class="toc">
        <h2>目录</h2>
        <ul>
    """

    # Collect all HTML files in order
    all_files = []
    for i in range(7):  # part0 to part6
        pattern = f"html_output/part{i}/*.html"
        files = glob.glob(pattern)
        all_files.extend(files)

    # Sort files
    all_files.sort(key=lambda x: (int(x.split('/part')[1].split('/')[0]), x))

    # Add TOC entries
    for html_file in all_files:
        base_name = os.path.basename(html_file).replace('.html', '')
        readable_name = base_name.replace('_', ' ')
        toc += f'<li><a href="#{base_name}">{readable_name}</a></li>'

    toc += """
        </ul>
    </div>
    """
    combined_content.append(toc)

    # Add content from all files
    for html_file in all_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract body content
            body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                # Remove the container div if present
                body_content = re.sub(r'<div class="container">(.*?)</div>', r'\1', body_content, flags=re.DOTALL)

                base_name = os.path.basename(html_file).replace('.html', '')
                combined_content.append(f'<div id="{base_name}">')
                combined_content.append(body_content)
                combined_content.append('</div>')
                combined_content.append('<div style="page-break-after: always;"></div>')
        except Exception as e:
            print(f"Error reading {html_file}: {e}")

    # Create combined HTML
    full_combined_content = '\n'.join(combined_content)

    template = create_html_template()
    combined_html = template.format(content=full_combined_content, title="《只有弱智才买股票》- 完整版")

    # Save combined HTML
    combined_file = "html_output/combined_all_parts.html"
    with open(combined_file, 'w', encoding='utf-8') as f:
        f.write(combined_html)

    print(f"✓ Created combined HTML: {combined_file}")
    return combined_file

def main():
    """Main conversion function"""
    print("=== Markdown to HTML Converter ===")
    print("Converting content from src/part0-src/part6 to HTML format")

    # Create output directory
    os.makedirs("html_output", exist_ok=True)
    print("✓ Created output directory: html_output")

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
        html_file = convert_md_file_to_html(md_file)
        if html_file:
            success_count += 1

    print(f"\n=== Individual Conversion Complete ===")
    print(f"Successfully converted: {success_count}/{total_count} files")

    # Create combined HTML
    if success_count > 0:
        print("\nCreating combined HTML file...")
        combined_file = create_combined_html()

        print(f"\n=== All Done! ===")
        print(f"Individual HTML files: html_output/")
        print(f"Combined HTML file: {combined_file}")
        print(f"\nTo convert to PDF, you can:")
        print(f"1. Open the HTML files in Chrome/Edge and print to PDF")
        print(f"2. Use online HTML to PDF converters")
        print(f"3. Install wkhtmltopdf and run: wkhtmltopdf {combined_file} output.pdf")

if __name__ == "__main__":
    main()