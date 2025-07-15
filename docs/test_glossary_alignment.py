#!/usr/bin/env python3
"""
Test Glossary Alignment
Open glossary page to check alignment issues
"""

import webbrowser
import os

def test_glossary_alignment():
    """Test the glossary page alignment"""
    print("=== Glossary Alignment Test ===")
    print("Opening glossary.html to check content alignment...")
    
    file_path = os.path.abspath('glossary.html')
    if os.path.exists(file_path):
        webbrowser.open(f"file://{file_path}#performance-metrics")
        print("✅ Opened glossary.html at Performance Metrics section")
        print("\n🔍 Please check if the alignment issue is fixed:")
        print("   ✓ Performance Metrics text should be fully visible")
        print("   ✓ Definition list items should not be cut off")
        print("   ✓ Content should align properly within the grey area")
        print("   ✓ Text should not overflow or get clipped")
        print("   ✓ Scroll to File System Features section to verify")
    else:
        print("❌ glossary.html not found")

if __name__ == "__main__":
    test_glossary_alignment()
