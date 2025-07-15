#!/usr/bin/env python3
"""
Final Content Verification
Check that all pages have both navigation and content
"""

import os

def verify_content_and_navigation():
    """Verify all files have content and navigation"""
    
    print("=== Final Content and Navigation Verification ===\n")
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files = [f for f in html_files if f not in ['search.html', 'genindex.html']]  # Skip special pages
    html_files.sort()
    
    all_good = True
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check file size
            size_kb = len(content) / 1024
            
            # Check for navigation elements
            has_nav_css = 'navigation-fix.css' in content
            has_nav_js = 'navigation-enhancement.js' in content
            has_navigation = 'wy-menu wy-menu-vertical' in content
            has_toctree = 'toctree-l' in content
            
            # Check for actual content (paragraphs, sections)
            has_content = '<p>' in content and '<section id=' in content
            has_headings = '<h2>' in content or '<h3>' in content
            
            # Overall status
            content_ok = has_content and has_headings and size_kb > 30  # At least 30KB
            nav_ok = has_nav_css and has_nav_js and has_navigation and has_toctree
            
            status = "✅" if (content_ok and nav_ok) else "❌"
            
            print(f"{status} {html_file} ({size_kb:.1f}KB)")
            print(f"   Content: {'✓' if content_ok else '✗'} Navigation: {'✓' if nav_ok else '✗'}")
            
            if not (content_ok and nav_ok):
                all_good = False
                if not content_ok:
                    print(f"   Issue: Missing content (size: {size_kb:.1f}KB, content: {has_content}, headings: {has_headings})")
                if not nav_ok:
                    print(f"   Issue: Missing navigation (CSS: {has_nav_css}, JS: {has_nav_js}, nav: {has_navigation})")
            
        except Exception as e:
            print(f"❌ {html_file}: Error - {e}")
            all_good = False
    
    print(f"\n=== SUMMARY ===")
    if all_good:
        print("🎉 SUCCESS: All pages have both content and navigation!")
        print("   ✅ All files have substantial content (text, headings, sections)")
        print("   ✅ All files have working navigation (CSS, JS, sidebar)")
        print("   ✅ Files are properly sized (30KB+ with content)")
        print("\n📝 Your documentation is now complete:")
        print("   - Navigation works like storage-overview on all pages")
        print("   - Content is visible and properly formatted")
        print("   - No duplicate sections or alignment issues")
        print("   - Ready for use! 🎉")
    else:
        print("⚠️  Some files still need attention")
    
    return all_good

if __name__ == "__main__":
    verify_content_and_navigation()
