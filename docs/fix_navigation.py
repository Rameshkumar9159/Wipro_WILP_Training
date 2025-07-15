#!/usr/bin/env python3
"""
Navigation Fix Script for Storage Systems Documentation
Author: T S Rameshkumar
Email: rameshsv06@gmail.com
Batch: WiproNGA_Datacentre_B9_25VID2182

This script fixes the navigation subtopics visibility issue by adding 
a navigation-fix.css file to all HTML documentation files.
"""

import os
import re
import sys
from pathlib import Path

def add_navigation_enhancements(html_file_path):
    """
    Add navigation-fix.css and navigation-enhancement.js to an HTML file if not already present.
    
    Args:
        html_file_path (str): Path to the HTML file to modify
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        modified = False
        
        # Check and add navigation-fix.css
        if 'navigation-fix.css' not in content:
            # Find the theme.css line and add navigation-fix.css after it
            css_pattern = r'(\s+<link rel="stylesheet" type="text/css" href="_static/css/theme\.css[^>]*" />)'
            
            if re.search(css_pattern, content):
                replacement = r'\1\n      <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css" />'
                content = re.sub(css_pattern, replacement, content, count=1)
                modified = True
            else:
                # Try custom-header-footer.css pattern
                css_pattern = r'(\s+<link rel="stylesheet" type="text/css" href="_static/css/custom-header-footer\.css" />)'
                if re.search(css_pattern, content):
                    replacement = r'\1\n      <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css" />'
                    content = re.sub(css_pattern, replacement, content, count=1)
                    modified = True
        
        # Check and add navigation-enhancement.js
        if 'navigation-enhancement.js' not in content:
            # Find the theme.js line and add navigation-enhancement.js after it
            js_pattern = r'(\s+<script src="_static/js/theme\.js"></script>)'
            
            if re.search(js_pattern, content):
                replacement = r'\1\n    <script src="_static/js/navigation-enhancement.js"></script>'
                content = re.sub(js_pattern, replacement, content, count=1)
                modified = True
        
        if modified:
            # Write the modified content back to the file
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"✓ {html_file_path}: Navigation enhancements added successfully")
            return True
        else:
            print(f"✓ {html_file_path}: Navigation enhancements already applied")
            return False
            
    except Exception as e:
        print(f"✗ {html_file_path}: Error - {str(e)}")
        return False

def main():
    """Main function to process all HTML files in the docs directory."""
    
    # Get the current directory (should be the docs directory)
    docs_dir = Path.cwd()
    
    print("=" * 60)
    print("Navigation Fix Script for Storage Systems Documentation")
    print("Author: T S Rameshkumar (rameshsv06@gmail.com)")
    print("Batch: WiproNGA_Datacentre_B9_25VID2182")
    print("=" * 60)
    print(f"Working directory: {docs_dir}")
    print()
    
    # Find all HTML files in the current directory
    html_files = list(docs_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in the current directory!")
        print("Make sure you're running this script from the docs directory.")
        sys.exit(1)
    
    print(f"Found {len(html_files)} HTML files to process...")
    print()
    
    # Process each HTML file
    modified_count = 0
    for html_file in html_files:
        if add_navigation_enhancements(html_file):
            modified_count += 1
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total HTML files processed: {len(html_files)}")
    print(f"Files modified: {modified_count}")
    print(f"Files already up-to-date: {len(html_files) - modified_count}")
    print()
    
    if modified_count > 0:
        print("✅ Navigation enhancements have been successfully applied!")
        print("🔍 The subtopics should now be visible in the navigation menu.")
        print("🚀 Enhanced JavaScript functionality has been added for better UX.")
        print("📂 You can now open any HTML file in your browser to test the fix.")
    else:
        print("ℹ️  All files were already up-to-date.")
    
    print()
    print("Note: If you still experience navigation issues, try:")
    print("1. Clear your browser cache")
    print("2. Hard refresh the page (Ctrl+F5)")
    print("3. Check browser console for any JavaScript errors")

if __name__ == "__main__":
    main()
