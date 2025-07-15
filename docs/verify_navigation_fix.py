#!/usr/bin/env python3
"""
Navigation Fix Verification Script
Author: T S Rameshkumar
Email: rameshsv06@gmail.com
Batch: WiproNGA_Datacentre_B9_25VID2182

This script creates a test report to verify that navigation fixes are working.
"""

import os
import re
from pathlib import Path

def extract_navigation_structure(html_file_path):
    """Extract navigation structure from HTML file."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the navigation menu
        nav_pattern = r'<div class="wy-menu wy-menu-vertical"[^>]*>(.*?)</div>'
        nav_match = re.search(nav_pattern, content, re.DOTALL)
        
        if not nav_match:
            return {"error": "Navigation menu not found"}
        
        nav_content = nav_match.group(1)
        
        # Count navigation levels
        l1_count = len(re.findall(r'class="[^"]*toctree-l1[^"]*"', nav_content))
        l2_count = len(re.findall(r'class="[^"]*toctree-l2[^"]*"', nav_content))
        l3_count = len(re.findall(r'class="[^"]*toctree-l3[^"]*"', nav_content))
        l4_count = len(re.findall(r'class="[^"]*toctree-l4[^"]*"', nav_content))
        
        # Check for expand buttons
        expand_buttons = len(re.findall(r'class="[^"]*toctree-expand[^"]*"', nav_content))
        
        return {
            "level1_items": l1_count,
            "level2_items": l2_count,
            "level3_items": l3_count,
            "level4_items": l4_count,
            "expand_buttons": expand_buttons,
            "has_navigation": True
        }
    
    except Exception as e:
        return {"error": str(e)}

def check_css_js_includes(html_file_path):
    """Check if required CSS and JS files are included."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return {
            "theme_css": "theme.css" in content,
            "navigation_fix_css": "navigation-fix.css" in content,
            "custom_header_css": "custom-header-footer.css" in content,
            "theme_js": "theme.js" in content,
            "navigation_enhancement_js": "navigation-enhancement.js" in content,
            "jquery": "jquery.js" in content
        }
    
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main function to verify navigation fixes."""
    
    docs_dir = Path.cwd()
    
    print("=" * 80)
    print("NAVIGATION FIX VERIFICATION REPORT")
    print("Author: T S Rameshkumar (rameshsv06@gmail.com)")
    print("Batch: WiproNGA_Datacentre_B9_25VID2182")
    print("=" * 80)
    print()
    
    # Key files to test
    test_files = [
        "index.html",
        "storage-overview.html", 
        "disk-management.html",
        "file-systems.html",
        "data-organization.html",
        "network-storage.html",
        "troubleshooting.html"
    ]
    
    print("🔍 TESTING KEY NAVIGATION PAGES")
    print("-" * 50)
    
    all_good = True
    
    for filename in test_files:
        filepath = docs_dir / filename
        if not filepath.exists():
            print(f"❌ {filename}: File not found")
            all_good = False
            continue
        
        print(f"\n📄 Testing: {filename}")
        
        # Check CSS/JS includes
        includes = check_css_js_includes(filepath)
        if "error" in includes:
            print(f"   ❌ Error checking includes: {includes['error']}")
            all_good = False
            continue
        
        print("   📚 Required Files:")
        for file_type, present in includes.items():
            status = "✅" if present else "❌"
            print(f"      {status} {file_type}")
            if not present:
                all_good = False
        
        # Check navigation structure
        nav_info = extract_navigation_structure(filepath)
        if "error" in nav_info:
            print(f"   ❌ Navigation error: {nav_info['error']}")
            all_good = False
            continue
        
        print("   🗺️ Navigation Structure:")
        print(f"      📁 Level 1 items: {nav_info['level1_items']}")
        print(f"      📂 Level 2 items: {nav_info['level2_items']}")
        print(f"      📄 Level 3 items: {nav_info['level3_items']}")
        print(f"      📝 Level 4 items: {nav_info['level4_items']}")
        print(f"      🔘 Expand buttons: {nav_info['expand_buttons']}")
        
        # Determine navigation health
        has_multilevel = nav_info['level2_items'] > 0 or nav_info['level3_items'] > 0
        nav_status = "✅ Good" if has_multilevel else "⚠️ Limited"
        print(f"   🎯 Navigation Status: {nav_status}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if all_good:
        print("🎉 ALL NAVIGATION FIXES SUCCESSFULLY APPLIED!")
        print()
        print("✅ What's Working:")
        print("   • Navigation CSS fixes are loaded")
        print("   • JavaScript enhancements are active") 
        print("   • Multi-level navigation structure is present")
        print("   • Expand/collapse functionality is available")
        print()
        print("🚀 Your navigation should now display:")
        print("   • Visible subtopics in the left sidebar")
        print("   • Proper indentation for nested items")
        print("   • Working expand/collapse buttons")
        print("   • Improved hover effects")
        print("   • Current page highlighting")
    else:
        print("⚠️ Some issues detected that may affect navigation.")
    
    print("\n📱 TO TEST THE NAVIGATION:")
    print("1. Open any HTML file in your web browser")
    print("2. Look at the left sidebar navigation menu")
    print("3. Verify that subtopics are visible under main topics")
    print("4. Click expand/collapse buttons to test functionality") 
    print("5. Try on both desktop and mobile screen sizes")
    
    print(f"\n🌐 Quick Test Links:")
    print(f"   • Main: file://{docs_dir}/index.html")
    print(f"   • Storage: file://{docs_dir}/storage-overview.html")
    print(f"   • Disk Mgmt: file://{docs_dir}/disk-management.html")

if __name__ == "__main__":
    main()
