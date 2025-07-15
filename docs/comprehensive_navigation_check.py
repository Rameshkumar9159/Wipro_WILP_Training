#!/usr/bin/env python3
"""
Comprehensive Navigation Check
Verifies that ALL HTML pages have identical navigation structure to storage-overview.html
"""

import os
import re
from bs4 import BeautifulSoup

def check_navigation_structure(file_path):
    """Check if a file has proper navigation structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        issues = []
        
        # Check for CSS injection
        css_link = soup.find('link', href='_static/css/navigation-fix.css')
        if not css_link:
            issues.append("Missing navigation-fix.css")
        
        # Check for JS injection
        js_script = soup.find('script', src='_static/js/navigation-enhancement.js')
        if not js_script:
            issues.append("Missing navigation-enhancement.js")
        
        # Check for navigation structure
        nav_element = soup.find('nav', {'data-toggle': 'wy-nav-shift'})
        if not nav_element:
            issues.append("Missing main navigation element")
        
        # Check for toctree with nested items
        toctree = soup.find('div', class_='toctree-wrapper')
        if not toctree:
            issues.append("Missing toctree-wrapper")
        else:
            # Check for nested ul elements (multi-level navigation)
            nested_lists = toctree.find_all('ul')
            if len(nested_lists) < 2:
                issues.append("Missing nested navigation lists")
            
            # Check for current page marking
            current_items = toctree.find_all('li', class_='current')
            if not current_items:
                issues.append("No current page marking found")
        
        return issues
    
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

def get_navigation_html(file_path):
    """Extract the navigation HTML for comparison"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        nav_element = soup.find('nav', {'data-toggle': 'wy-nav-shift'})
        if nav_element:
            return str(nav_element)
        return None
    except:
        return None

def main():
    print("=== Comprehensive Navigation Structure Check ===\n")
    
    # Get all HTML files
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    # Use storage-overview.html as the reference
    reference_file = 'storage-overview.html'
    if reference_file not in html_files:
        print(f"ERROR: Reference file {reference_file} not found!")
        return
    
    print(f"Using {reference_file} as navigation reference\n")
    
    # Get reference navigation
    reference_nav = get_navigation_html(reference_file)
    reference_issues = check_navigation_structure(reference_file)
    
    print(f"Reference file ({reference_file}) issues: {reference_issues or 'None'}\n")
    
    all_good = True
    files_with_issues = []
    
    for html_file in html_files:
        if html_file == reference_file:
            continue
            
        print(f"Checking {html_file}...")
        issues = check_navigation_structure(html_file)
        
        if issues:
            print(f"  ❌ Issues found: {', '.join(issues)}")
            files_with_issues.append((html_file, issues))
            all_good = False
        else:
            # Check if navigation structure matches reference
            current_nav = get_navigation_html(html_file)
            if current_nav and reference_nav:
                # Compare key structural elements
                ref_soup = BeautifulSoup(reference_nav, 'html.parser')
                cur_soup = BeautifulSoup(current_nav, 'html.parser')
                
                ref_lists = len(ref_soup.find_all('ul'))
                cur_lists = len(cur_soup.find_all('ul'))
                
                if ref_lists != cur_lists:
                    print(f"  ⚠️  Navigation structure differs (lists: {cur_lists} vs reference: {ref_lists})")
                    files_with_issues.append((html_file, [f"Navigation structure differs"]))
                    all_good = False
                else:
                    print(f"  ✅ Navigation structure OK")
            else:
                print(f"  ⚠️  Could not compare navigation structure")
                files_with_issues.append((html_file, ["Could not extract navigation"]))
                all_good = False
    
    print("\n=== SUMMARY ===")
    if all_good:
        print("✅ All files have proper navigation structure!")
    else:
        print(f"❌ {len(files_with_issues)} files need attention:")
        for file, issues in files_with_issues:
            print(f"  - {file}: {', '.join(issues)}")
    
    return files_with_issues

if __name__ == "__main__":
    files_with_issues = main()
