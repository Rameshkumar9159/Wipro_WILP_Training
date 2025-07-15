#!/usr/bin/env python3
"""
HTML Structure Fix Script for Storage Systems Documentation
Author: T S Rameshkumar
Email: rameshsv06@gmail.com
Batch: WiproNGA_Datacentre_B9_25VID2182

This script checks and fixes HTML structure issues and ensures navigation fixes are applied.
"""

import os
import re
import sys
from pathlib import Path

def check_html_structure(html_file_path):
    """
    Check if HTML file has proper structure.
    
    Args:
        html_file_path (str): Path to the HTML file to check
        
    Returns:
        bool: True if structure is valid, False otherwise
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check for proper DOCTYPE
        if not content.startswith('<!DOCTYPE html>'):
            return False
        
        # Check for proper head section
        if '<head>' not in content or '</head>' not in content:
            return False
        
        # Check for proper body section
        if '<body' not in content or '</body>' not in content:
            return False
        
        # Check if meta tags are in the right place (inside head)
        head_start = content.find('<head>')
        head_end = content.find('</head>')
        body_start = content.find('<body')
        
        if head_start == -1 or head_end == -1 or body_start == -1:
            return False
        
        # Check if there are meta tags outside head section
        meta_before_head = content[:head_start].count('<meta')
        meta_after_head_before_body = content[head_end:body_start].count('<meta')
        
        if meta_before_head > 0 or meta_after_head_before_body > 0:
            return False
        
        return True
    
    except Exception as e:
        print(f"Error checking {html_file_path}: {e}")
        return False

def fix_html_structure(html_file_path):
    """
    Attempt to fix HTML structure issues.
    
    Args:
        html_file_path (str): Path to the HTML file to fix
        
    Returns:
        bool: True if file was fixed, False otherwise
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Look for misplaced meta tags and sections before DOCTYPE
        # This is a common issue we're seeing
        
        # Find where the actual HTML should start
        doctype_match = re.search(r'<!DOCTYPE html>', content)
        if not doctype_match:
            return False
        
        doctype_start = doctype_match.start()
        
        # If there's content before DOCTYPE, it might be misplaced body content
        if doctype_start > 0:
            # Extract content before DOCTYPE
            misplaced_content = content[:doctype_start]
            proper_html = content[doctype_start:]
            
            # Look for section tags in misplaced content
            if '<section' in misplaced_content:
                # This content should be in the body
                # Find where to insert it in the body
                body_content_start = proper_html.find('<div itemprop="articleBody">')
                if body_content_start != -1:
                    # Insert the misplaced content after articleBody div
                    insert_point = proper_html.find('>', body_content_start) + 1
                    new_content = (proper_html[:insert_point] + '\n' + 
                                 misplaced_content + '\n' + 
                                 proper_html[insert_point:])
                    content = new_content
        
        # Ensure navigation enhancements are present
        if 'navigation-fix.css' not in content:
            # Add CSS after theme.css
            css_pattern = r'(\s+<link rel="stylesheet" type="text/css" href="_static/css/theme\.css[^>]*" />)'
            if re.search(css_pattern, content):
                content = re.sub(css_pattern, 
                               r'\1\n      <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css" />', 
                               content, count=1)
        
        if 'navigation-enhancement.js' not in content:
            # Add JS after theme.js
            js_pattern = r'(\s+<script src="_static/js/theme\.js"></script>)'
            if re.search(js_pattern, content):
                content = re.sub(js_pattern, 
                               r'\1\n    <script src="_static/js/navigation-enhancement.js"></script>', 
                               content, count=1)
        
        # Only write if content changed
        if content != original_content:
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error fixing {html_file_path}: {e}")
        return False

def verify_navigation_enhancements(html_file_path):
    """
    Verify that navigation enhancements are properly applied.
    
    Args:
        html_file_path (str): Path to the HTML file to verify
        
    Returns:
        dict: Status of various enhancements
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return {
            'navigation_css': 'navigation-fix.css' in content,
            'navigation_js': 'navigation-enhancement.js' in content,
            'custom_css': 'custom-header-footer.css' in content,
            'theme_css': 'theme.css' in content,
            'theme_js': 'theme.js' in content
        }
    
    except Exception as e:
        return {'error': str(e)}

def main():
    """Main function to check and fix all HTML files."""
    
    docs_dir = Path.cwd()
    
    print("=" * 70)
    print("HTML Structure Fix & Navigation Enhancement Verification")
    print("Author: T S Rameshkumar (rameshsv06@gmail.com)")
    print("Batch: WiproNGA_Datacentre_B9_25VID2182")
    print("=" * 70)
    print(f"Working directory: {docs_dir}")
    print()
    
    # Find all HTML files
    html_files = list(docs_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found!")
        sys.exit(1)
    
    print(f"Found {len(html_files)} HTML files to check...")
    print()
    
    # Check each file
    structure_issues = 0
    enhancement_issues = 0
    fixed_files = 0
    
    for html_file in html_files:
        print(f"Checking: {html_file.name}")
        
        # Check structure
        structure_ok = check_html_structure(html_file)
        if not structure_ok:
            print(f"  ⚠️  Structure issues detected")
            if fix_html_structure(html_file):
                print(f"  ✅ Structure fixed")
                fixed_files += 1
            else:
                print(f"  ❌ Could not fix structure")
                structure_issues += 1
        else:
            print(f"  ✅ Structure OK")
        
        # Check enhancements
        enhancements = verify_navigation_enhancements(html_file)
        if 'error' in enhancements:
            print(f"  ❌ Error checking enhancements: {enhancements['error']}")
            enhancement_issues += 1
        else:
            missing = []
            if not enhancements['navigation_css']:
                missing.append('navigation-fix.css')
            if not enhancements['navigation_js']:
                missing.append('navigation-enhancement.js')
            
            if missing:
                print(f"  ⚠️  Missing: {', '.join(missing)}")
                # Try to fix
                if fix_html_structure(html_file):
                    print(f"  ✅ Enhancements added")
                    fixed_files += 1
                else:
                    enhancement_issues += 1
            else:
                print(f"  ✅ All enhancements present")
        
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total files checked: {len(html_files)}")
    print(f"Files fixed: {fixed_files}")
    print(f"Structure issues remaining: {structure_issues}")
    print(f"Enhancement issues remaining: {enhancement_issues}")
    print()
    
    if structure_issues == 0 and enhancement_issues == 0:
        print("🎉 All files are now properly configured!")
        print("📱 Navigation should work correctly on all pages.")
    else:
        print(f"⚠️  Some issues remain that need manual attention.")
    
    print("\n📝 To test the navigation fix:")
    print("1. Open any HTML file in a web browser")
    print("2. Check that subtopics are visible in the left navigation")
    print("3. Verify that clicking on main topics expands/collapses subtopics")
    print("4. Test navigation on both desktop and mobile views")

if __name__ == "__main__":
    main()
