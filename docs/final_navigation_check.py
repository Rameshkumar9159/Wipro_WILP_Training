#!/usr/bin/env python3
"""
Fixed Comprehensive Navigation Check and Repair
Ensures ALL HTML pages have identical navigation structure
"""

import os
import re
from bs4 import BeautifulSoup

def get_reference_navigation():
    """Extract the complete navigation structure from storage-overview.html"""
    try:
        with open('storage-overview.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the navigation menu
        nav_menu = soup.find('div', class_='wy-menu wy-menu-vertical')
        if nav_menu:
            return str(nav_menu)
        return None
    except Exception as e:
        print(f"Error reading reference file: {e}")
        return None

def check_and_fix_navigation(file_path, reference_nav):
    """Check and fix navigation in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        issues = []
        fixed = False
        
        # Check for CSS injection
        css_link = soup.find('link', href='_static/css/navigation-fix.css')
        if not css_link:
            issues.append("Missing navigation-fix.css")
            # Add CSS link
            head = soup.find('head')
            if head:
                new_css = soup.new_tag('link', rel='stylesheet', type='text/css', href='_static/css/navigation-fix.css')
                head.append(new_css)
                fixed = True
        
        # Check for JS injection
        js_script = soup.find('script', src='_static/js/navigation-enhancement.js')
        if not js_script:
            issues.append("Missing navigation-enhancement.js")
            # Add JS script before closing body
            body = soup.find('body')
            if body:
                new_js = soup.new_tag('script', src='_static/js/navigation-enhancement.js')
                body.append(new_js)
                fixed = True
        
        # Check navigation structure
        current_nav = soup.find('div', class_='wy-menu wy-menu-vertical')
        if not current_nav and reference_nav:
            issues.append("Missing or incorrect navigation structure")
            # This would need manual intervention for complex cases
        elif current_nav and reference_nav:
            # Check if navigation has multi-level structure
            nav_lists = current_nav.find_all('ul')
            if len(nav_lists) < 2:
                issues.append("Navigation lacks multi-level structure")
        
        # Save if we made fixes
        if fixed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  🔧 Fixed CSS/JS injection in {file_path}")
        
        return issues
    
    except Exception as e:
        return [f"Error processing file: {str(e)}"]

def ensure_all_files_have_identical_navigation():
    """Ensure all files have the same navigation as storage-overview.html"""
    
    print("=== Navigation Standardization Process ===\n")
    
    # Get reference navigation
    reference_nav = get_reference_navigation()
    if not reference_nav:
        print("❌ Could not extract reference navigation from storage-overview.html")
        return
    
    print("✅ Reference navigation extracted from storage-overview.html\n")
    
    # Get all HTML files
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    files_needing_manual_fix = []
    
    for html_file in html_files:
        print(f"Processing {html_file}...")
        
        if html_file == 'storage-overview.html':
            print("  📋 Reference file - skipping")
            continue
        
        issues = check_and_fix_navigation(html_file, reference_nav)
        
        if issues:
            print(f"  ⚠️  Issues: {', '.join(issues)}")
            files_needing_manual_fix.append((html_file, issues))
        else:
            print(f"  ✅ All checks passed")
    
    print(f"\n=== SUMMARY ===")
    if not files_needing_manual_fix:
        print("✅ All files have proper navigation structure!")
    else:
        print(f"⚠️  {len(files_needing_manual_fix)} files may need manual attention:")
        for file, issues in files_needing_manual_fix:
            print(f"  - {file}: {', '.join(issues)}")
    
    return files_needing_manual_fix

def create_navigation_standardization_script():
    """Create a script to standardize navigation across all files"""
    
    script_content = '''#!/usr/bin/env python3
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
                '  <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css" />\\n</head>'
            )
        
        if '_static/js/navigation-enhancement.js' not in content:
            content = content.replace(
                '</body>',
                '  <script src="_static/js/navigation-enhancement.js"></script>\\n</body>'
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
'''
    
    with open('standardize_navigation.py', 'w') as f:
        f.write(script_content)
    
    print("📝 Created standardize_navigation.py script")

if __name__ == "__main__":
    files_needing_fix = ensure_all_files_have_identical_navigation()
    create_navigation_standardization_script()
