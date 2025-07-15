#!/usr/bin/env python3
"""
Quick Glossary Content Width Test
"""

import webbrowser
import os

def test_glossary_content_width():
    """Test glossary content width and text clipping"""
    print("=== Glossary Content Width Test ===")
    
    file_path = os.path.abspath('glossary.html')
    if os.path.exists(file_path):
        # Open at the specific problematic section
        webbrowser.open(f"file://{file_path}#common-command-abbreviations")
        print("✅ Opened glossary.html at Common Command Abbreviations section")
        print("\n🔍 Please verify the content width fixes:")
        print("   ✓ Common Command Abbreviations - text should not be cut off")
        print("   ✓ Storage Unit Definitions - full content visible")
        print("   ✓ Performance Metrics - proper text flow")
        print("   ✓ RAID Levels Reference - no text clipping")
        print("   ✓ Network Storage Protocols - content aligned properly")
        print("   ✓ File System Features - all text visible")
        print("\n📱 Test on different screen sizes to ensure responsive layout works")
    else:
        print("❌ glossary.html not found")

if __name__ == "__main__":
    test_glossary_content_width()
