#!/usr/bin/env python3
"""
Navigation Standardization Script
Updates all HTML files to have consistent navigation structure
"""

import os
import re
from bs4 import BeautifulSoup

def standardize_navigation_in_file(file_path):
    """Standardize navigation in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure CSS and JS are included
        if '_static/css/navigation-fix.css' not in content:
            content = content.replace(
                '</head>',
                '  <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css" />\n</head>'
            )
        
        if '_static/js/navigation-enhancement.js' not in content:
            content = content.replace(
                '</body>',
                '  <script src="_static/js/navigation-enhancement.js"></script>\n</body>'
            )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for html_file in html_files:
        print(f"Standardizing {html_file}...")
        if standardize_navigation_in_file(html_file):
            print(f"  ✅ {html_file} updated")
        else:
            print(f"  ❌ Failed to update {html_file}")

if __name__ == "__main__":
    main()
