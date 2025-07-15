#!/usr/bin/env python3
"""
Final Verification: Ensure ALL pages have identical navigation experience
"""

import os
from bs4 import BeautifulSoup

def extract_navigation_details(file_path):
    """Extract detailed navigation information from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        details = {
            'file': file_path,
            'has_nav_css': bool(soup.find('link', href='_static/css/navigation-fix.css')),
            'has_nav_js': bool(soup.find('script', src='_static/js/navigation-enhancement.js')),
            'nav_menu': soup.find('div', class_='wy-menu wy-menu-vertical'),
            'nav_lists_count': 0,
            'toctree_levels': [],
            'current_items': 0,
            'has_captions': False
        }
        
        if details['nav_menu']:
            # Count navigation lists
            nav_lists = details['nav_menu'].find_all('ul')
            details['nav_lists_count'] = len(nav_lists)
            
            # Find toctree levels
            for li in details['nav_menu'].find_all('li'):
                classes = li.get('class', [])
                for cls in classes:
                    if cls.startswith('toctree-l'):
                        level = cls.replace('toctree-l', '')
                        if level not in details['toctree_levels']:
                            details['toctree_levels'].append(level)
            
            # Count current items
            current_items = details['nav_menu'].find_all('li', class_='current')
            details['current_items'] = len(current_items)
            
            # Check for captions
            captions = details['nav_menu'].find_all('p', class_='caption')
            details['has_captions'] = len(captions) > 0
        
        details['toctree_levels'].sort()
        
        return details
    
    except Exception as e:
        return {'file': file_path, 'error': str(e)}

def compare_navigation_structures(reference_details, file_details):
    """Compare navigation structures and return differences"""
    differences = []
    
    if not file_details.get('has_nav_css'):
        differences.append("Missing navigation CSS")
    
    if not file_details.get('has_nav_js'):
        differences.append("Missing navigation JS")
    
    if file_details.get('nav_lists_count', 0) != reference_details.get('nav_lists_count', 0):
        differences.append(f"Different nav list count: {file_details.get('nav_lists_count')} vs reference {reference_details.get('nav_lists_count')}")
    
    if file_details.get('toctree_levels') != reference_details.get('toctree_levels'):
        differences.append(f"Different toctree levels: {file_details.get('toctree_levels')} vs reference {reference_details.get('toctree_levels')}")
    
    if not file_details.get('has_captions') and reference_details.get('has_captions'):
        differences.append("Missing navigation captions")
    
    return differences

def main():
    print("=== Final Navigation Verification ===\n")
    
    # Get all HTML files
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    # Use storage-overview.html as reference
    reference_file = 'storage-overview.html'
    
    print(f"Extracting reference navigation from {reference_file}...")
    reference_details = extract_navigation_details(reference_file)
    
    if 'error' in reference_details:
        print(f"❌ Error reading reference file: {reference_details['error']}")
        return
    
    print(f"Reference navigation structure:")
    print(f"  - Navigation lists: {reference_details['nav_lists_count']}")
    print(f"  - Toctree levels: {reference_details['toctree_levels']}")
    print(f"  - Current items: {reference_details['current_items']}")
    print(f"  - Has captions: {reference_details['has_captions']}")
    print(f"  - Has CSS: {reference_details['has_nav_css']}")
    print(f"  - Has JS: {reference_details['has_nav_js']}")
    print()
    
    all_identical = True
    files_with_differences = []
    
    for html_file in html_files:
        if html_file == reference_file:
            continue
        
        print(f"Checking {html_file}...")
        file_details = extract_navigation_details(html_file)
        
        if 'error' in file_details:
            print(f"  ❌ Error: {file_details['error']}")
            all_identical = False
            continue
        
        differences = compare_navigation_structures(reference_details, file_details)
        
        if differences:
            print(f"  ⚠️  Differences found: {', '.join(differences)}")
            files_with_differences.append((html_file, differences))
            all_identical = False
        else:
            print(f"  ✅ Navigation matches reference")
    
    print(f"\n=== FINAL SUMMARY ===")
    if all_identical:
        print("🎉 SUCCESS: All pages have identical navigation structure!")
        print("   - All pages include navigation CSS and JS")
        print("   - All pages have consistent multi-level navigation")
        print("   - Navigation experience is uniform across the documentation")
    else:
        print(f"⚠️  {len(files_with_differences)} pages still have differences:")
        for file, diffs in files_with_differences:
            print(f"  - {file}: {', '.join(diffs)}")
    
    # Additional check: Verify key files work properly
    print(f"\n=== KEY FILE VERIFICATION ===")
    key_files = ['index.html', 'storage-overview.html', 'disk-management.html', 'file-systems.html']
    
    for key_file in key_files:
        if key_file in [f[0] for f in files_with_differences]:
            print(f"❌ {key_file}: Has navigation issues")
        else:
            print(f"✅ {key_file}: Navigation working correctly")

if __name__ == "__main__":
    main()
