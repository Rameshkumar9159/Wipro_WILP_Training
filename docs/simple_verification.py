#!/usr/bin/env python3
"""Simple final verification script"""

import os

def main():
    print("=== Simple Navigation Verification ===")
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    print(f"Found {len(html_files)} HTML files")
    
    all_good = True
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_css = 'navigation-fix.css' in content
            has_js = 'navigation-enhancement.js' in content
            has_nav = 'wy-menu wy-menu-vertical' in content
            has_toctree = 'toctree-l' in content
            
            status = "✅" if (has_css and has_js and has_nav) else "❌"
            
            print(f"{status} {html_file}: CSS={has_css}, JS={has_js}, Nav={has_nav}, Toctree={has_toctree}")
            
            if not (has_css and has_js and has_nav):
                all_good = False
                
        except Exception as e:
            print(f"❌ {html_file}: Error - {e}")
            all_good = False
    
    print(f"\n=== SUMMARY ===")
    if all_good:
        print("🎉 All files have proper navigation structure!")
    else:
        print("⚠️  Some files need attention")

if __name__ == "__main__":
    main()
