#!/usr/bin/env python3
"""
Quick UI Test - Check that duplicate content is fixed
"""

import webbrowser
import os

def test_clean_ui():
    """Test that the UI is now clean without duplicates"""
    print("=== UI Cleanup Verification ===")
    print("Opening disk-management.html to verify clean UI...")
    
    file_path = os.path.abspath('disk-management.html')
    if os.path.exists(file_path):
        webbrowser.open(f"file://{file_path}")
        print("✅ Opened disk-management.html")
        print("\n🔍 Please verify:")
        print("   ✓ Single clean header (not multiple)")
        print("   ✓ No duplicate content sections")
        print("   ✓ Navigation sidebar works properly") 
        print("   ✓ Page loads quickly (small file size)")
        print("   ✓ Content is not repeated multiple times")
    else:
        print("❌ disk-management.html not found")

if __name__ == "__main__":
    test_clean_ui()
