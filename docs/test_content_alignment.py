#!/usr/bin/env python3
"""
Test Content Alignment in Glossary
Specifically test alignment issues in resources/glossary sections
"""

import webbrowser
import os

def test_content_alignment():
    """Test content alignment in glossary page"""
    print("=== Content Alignment Test for Glossary/Resources ===")
    
    file_path = os.path.abspath('glossary.html')
    if os.path.exists(file_path):
        webbrowser.open(f"file://{file_path}")
        print("✅ Opened glossary.html for alignment testing")
        print("\n🔍 Please check content alignment specifically:")
        print("   ✓ Content should be left-aligned within the grey content area")
        print("   ✓ Text should not be centered or floating strangely")
        print("   ✓ Definition lists should align properly with the left margin")
        print("   ✓ Common Command Abbreviations section alignment")
        print("   ✓ Storage Unit Definitions section alignment")  
        print("   ✓ Performance Metrics section alignment")
        print("   ✓ File System Features section alignment")
        print("\n📐 Check that:")
        print("   - Content starts properly from the left edge")
        print("   - No weird spacing or indentation issues")
        print("   - Text flows naturally within the content area")
        print("   - All sections have consistent alignment")
    else:
        print("❌ glossary.html not found")

if __name__ == "__main__":
    test_content_alignment()
