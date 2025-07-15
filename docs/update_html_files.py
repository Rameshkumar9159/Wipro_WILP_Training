#!/usr/bin/env python3
"""
Script to add custom header and footer to all HTML documentation files
Author: T S Rameshkumar
Batch: WiproNGA_Datacentre_B9_25VID2182
"""

import os
import re
from pathlib import Path

def get_page_title(html_content):
    """Extract page title from HTML title tag"""
    title_match = re.search(r'<title>([^—]*)', html_content)
    if title_match:
        return title_match.group(1).strip()
    return "Documentation"

def add_custom_styles(html_content):
    """Add custom CSS link to HTML head"""
    # Check if custom CSS is already added
    if 'custom-header-footer.css' in html_content:
        return html_content
    
    pattern = r'(<link rel="stylesheet" type="text/css" href="_static/css/theme\.css[^>]*>)'
    replacement = r'\1\n      <link rel="stylesheet" type="text/css" href="_static/css/custom-header-footer.css" />'
    return re.sub(pattern, replacement, html_content)

def add_header(html_content, page_title):
    """Add custom header after main content div"""
    header_html = f'''  <!-- Custom Header with Author and Batch Information -->
  <div class="document-header">
    <h1>{page_title}</h1>
    <div class="author-info">Name: T S Rameshkumar &lt;rameshsv06@gmail.com&gt;</div>
    <div class="batch-info">Batch: WiproNGA_Datacentre_B9_25VID2182</div>
  </div>

'''
    
    # Pattern to find the main content div
    pattern = r'(<div role="main" class="document"[^>]*>\s*<div itemprop="articleBody">\s*)\n\s*(<section id="[^"]*">)'
    replacement = f'\\1\n{header_html}\\2'
    return re.sub(pattern, replacement, html_content, flags=re.MULTILINE)

def remove_duplicate_h1(html_content, page_title):
    """Remove duplicate h1 title that's now in the header"""
    # Pattern to match the h1 with headerlink
    pattern = f'<h1>{re.escape(page_title)}<a class="headerlink"[^>]*></a></h1>\\s*\n'
    return re.sub(pattern, '', html_content)

def add_footer(html_content, page_title):
    """Add custom footer before closing main content div"""
    footer_html = f'''
<!-- Custom Footer with Author and Batch Information -->
<div class="document-footer">
  <div class="footer-content">
    <div class="author-details">
      <strong>Author:</strong> T S Rameshkumar<br>
      <strong>Email:</strong> rameshsv06@gmail.com
    </div>
    <div class="batch-details">
      <strong>Batch:</strong> WiproNGA_Datacentre_B9_25VID2182<br>
      <strong>Program:</strong> Wipro NGA Datacentre
    </div>
  </div>
  <div class="copyright">
    © 2025 T S Rameshkumar | {page_title} | Wipro NGA Datacentre Training
  </div>
</div>
'''
    
    # Pattern to find the end of content sections before closing divs
    pattern = r'(</section>\s*</section>\s*)\n\s*(</div>\s*</div>)'
    replacement = f'\\1\n{footer_html}\n\\2'
    return re.sub(pattern, replacement, html_content, flags=re.MULTILINE)

def update_copyright(html_content):
    """Update the existing copyright footer"""
    pattern = r'<p>&#169; Copyright 2025, [^<]*</p>'
    replacement = '<p>&#169; Copyright 2025, T S Rameshkumar &lt;rameshsv06@gmail.com&gt; | Batch: WiproNGA_Datacentre_B9_25VID2182.</p>'
    return re.sub(pattern, replacement, html_content)

def process_html_file(file_path):
    """Process a single HTML file to add header and footer"""
    print(f"Processing: {file_path}")
    
    # Skip certain files that have different structures
    skip_files = ['genindex.html', 'search.html', 'py-modindex.html']
    if any(skip in file_path.name for skip in skip_files):
        print(f"Skipping {file_path.name} (special structure)")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract page title
        page_title = get_page_title(content)
        print(f"  Title: {page_title}")
        
        # Apply transformations
        content = add_custom_styles(content)
        content = add_header(content, page_title)
        content = remove_duplicate_h1(content, page_title)
        content = add_footer(content, page_title)
        content = update_copyright(content)
        
        # Write back the modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Updated successfully")
        
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")

def main():
    """Main function to process all HTML files"""
    docs_dir = Path('/home/rameshkumar/Wipro_WILP_Training/docs')
    
    # Find all HTML files in the main docs directory (exclude subdirectories)
    html_files = [f for f in docs_dir.glob('*.html') if f.is_file()]
    
    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 50)
    
    for html_file in html_files:
        process_html_file(html_file)
        print()
    
    print("=" * 50)
    print("Processing complete!")

if __name__ == "__main__":
    main()
