#!/usr/bin/env python3
"""
Final Layout Test - Check grey content area alignment
"""

import webbrowser
import os

def test_layout_alignment():
    """Test that the grey content area is properly aligned"""
    print("=== Final Layout Alignment Test ===")
    print("Opening disk-management.html to verify layout alignment...")
    
    file_path = os.path.abspath('disk-management.html')
    if os.path.exists(file_path):
        webbrowser.open(f"file://{file_path}")
        print("✅ Opened disk-management.html")
        print("\n🔍 Please verify the layout is now correct:")
        print("   ✓ Grey content area (main content) is properly aligned")
        print("   ✓ Navigation sidebar is positioned correctly on the left") 
        print("   ✓ Content doesn't overlap or misalign")
        print("   ✓ No duplicate content sections")
        print("   ✓ Responsive layout works on different screen sizes")
        print("   ✓ Content area has proper margins and padding")
        
        print("\n📱 Test on different screen sizes:")
        print("   - Desktop: Content should be centered with sidebar on left")
        print("   - Tablet: Navigation should collapse/expand properly")
        print("   - Mobile: Content should stack properly")
    else:
        print("❌ disk-management.html not found")

if __name__ == "__main__":
    test_layout_alignment()
