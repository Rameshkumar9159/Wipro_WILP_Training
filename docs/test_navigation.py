#!/usr/bin/env python3
"""
Quick Navigation Test Script
Author: T S Rameshkumar
Email: rameshsv06@gmail.com
Batch: WiproNGA_Datacentre_B9_25VID2182

This script opens multiple documentation pages for quick navigation testing.
"""

import webbrowser
import os
import time
from pathlib import Path

def main():
    """Open key documentation pages for navigation testing."""
    
    docs_dir = Path.cwd()
    
    print("🚀 QUICK NAVIGATION TEST")
    print("=" * 40)
    print("Author: T S Rameshkumar")
    print("Batch: WiproNGA_Datacentre_B9_25VID2182")
    print("=" * 40)
    print()
    
    # Key pages to test
    test_pages = [
        ("Main Page", "index.html"),
        ("Storage Overview", "storage-overview.html"),
        ("Disk Management", "disk-management.html"),
        ("File Systems", "file-systems.html"),
        ("Network Storage", "network-storage.html")
    ]
    
    print("📱 Opening test pages in your default browser...")
    print("Check each page for:")
    print("  ✅ Visible subtopics in left navigation")
    print("  ✅ Proper indentation and hierarchy")
    print("  ✅ Current page highlighting")
    print("  ✅ Working hover effects")
    print()
    
    for page_name, filename in test_pages:
        filepath = docs_dir / filename
        if filepath.exists():
            file_url = f"file://{filepath.absolute()}"
            print(f"🌐 Opening: {page_name}")
            try:
                webbrowser.open(file_url)
                time.sleep(1)  # Small delay between opens
            except Exception as e:
                print(f"   ❌ Error opening {filename}: {e}")
        else:
            print(f"   ❌ File not found: {filename}")
    
    print()
    print("🔍 NAVIGATION TEST CHECKLIST:")
    print("=" * 40)
    print("For each opened page, verify:")
    print()
    print("1. 📋 LEFT SIDEBAR NAVIGATION:")
    print("   □ All main topics are visible")
    print("   □ Subtopics are visible under main topics")
    print("   □ Current page is highlighted (blue border)")
    print("   □ Navigation items have proper indentation")
    print()
    print("2. 🖱️ INTERACTION TESTING:")
    print("   □ Hover effects work on navigation items")
    print("   □ Clicking navigation links works")
    print("   □ Smooth scrolling to sections")
    print()
    print("3. 📱 RESPONSIVE TESTING:")
    print("   □ Resize browser window to test mobile view")
    print("   □ Navigation collapses/expands properly")
    print("   □ All items remain accessible")
    print()
    print("4. 🏃‍♂️ PERFORMANCE:")
    print("   □ Pages load quickly")
    print("   □ Navigation updates smoothly")
    print("   □ No JavaScript errors in browser console")
    print()
    
    print("✅ If all items check out, the navigation fix is working perfectly!")
    print()
    print("🚨 If you notice any issues:")
    print("1. Clear browser cache (Ctrl+F5)")
    print("2. Check browser console for errors (F12)")
    print("3. Verify all CSS/JS files are loading")
    print("4. Test with different browsers")

if __name__ == "__main__":
    main()
