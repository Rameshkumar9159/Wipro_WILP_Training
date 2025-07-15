#!/usr/bin/env python3
"""
Test current glossary alignment and content width
Author: T S Rameshkumar
Batch: WiproNGA_Datacentre_B9_25VID2182
Purpose: Check if the Common Command Abbreviations section is now properly aligned
"""

import re
import os

def test_glossary_structure():
    """Test the current structure and CSS application"""
    
    glossary_path = "/home/ramesh/Wipro_WILP_Training/docs/glossary.html"
    
    if not os.path.exists(glossary_path):
        print("Error: glossary.html not found")
        return
    
    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== GLOSSARY STRUCTURE ANALYSIS ===\n")
    
    # Check for CSS injection
    if 'navigation-fix.css' in content:
        print("✓ Custom CSS is injected")
    else:
        print("✗ Custom CSS not found")
    
    # Check for duplicate sections
    section_pattern = r'<section id="([^"]+)">'
    sections = re.findall(section_pattern, content)
    unique_sections = set(sections)
    
    print(f"Total sections: {len(sections)}")
    print(f"Unique sections: {len(unique_sections)}")
    
    if len(sections) == len(unique_sections):
        print("✓ No duplicate sections")
    else:
        print("✗ Still have duplicate sections")
        duplicates = [s for s in sections if sections.count(s) > 1]
        print(f"Duplicates: {set(duplicates)}")
    
    # Check Common Command Abbreviations section structure
    cca_pattern = r'<section id="common-command-abbreviations">(.*?)</section>'
    cca_match = re.search(cca_pattern, content, re.DOTALL)
    
    if cca_match:
        print("\n✓ Common Command Abbreviations section found")
        cca_content = cca_match.group(1)
        
        # Count definition items
        dt_count = len(re.findall(r'<dt[^>]*>', cca_content))
        dd_count = len(re.findall(r'<dd[^>]*>', cca_content))
        
        print(f"Definition terms (dt): {dt_count}")
        print(f"Definition descriptions (dd): {dd_count}")
        
        if dt_count == dd_count and dt_count > 0:
            print("✓ Balanced dt/dd structure")
        else:
            print("✗ Unbalanced dt/dd structure")
        
        # Check for proper CSS classes
        if 'class="simple glossary"' in cca_content:
            print("✓ Proper CSS classes applied")
        else:
            print("✗ Missing CSS classes")
            
    else:
        print("\n✗ Common Command Abbreviations section not found")
    
    # Check overall document structure
    print("\n=== DOCUMENT STRUCTURE ===")
    
    # Check for proper content wrapper
    if 'class="wy-nav-content"' in content:
        print("✓ Navigation content wrapper present")
    else:
        print("✗ Navigation content wrapper missing")
    
    # Check for rst-content class
    if 'class="rst-content"' in content:
        print("✓ RST content wrapper present")
    else:
        print("✗ RST content wrapper missing")
    
    # Check for main document structure
    doc_pattern = r'<div class="document">'
    if re.search(doc_pattern, content):
        print("✓ Document wrapper present")
    else:
        print("✗ Document wrapper missing")
    
    print("\n=== CSS ANALYSIS ===")
    
    # Check for style injections
    style_count = content.count('<style>')
    link_css_count = content.count('navigation-fix.css')
    
    print(f"Inline style blocks: {style_count}")
    print(f"Custom CSS links: {link_css_count}")
    
    if link_css_count > 0:
        print("✓ Custom CSS is linked")
    else:
        print("✗ Custom CSS not linked")

def create_html_test_page():
    """Create a test page to verify alignment visually"""
    
    test_html = """<!DOCTYPE html>
<html>
<head>
    <title>Glossary Alignment Test</title>
    <link rel="stylesheet" type="text/css" href="_static/css/navigation-fix.css">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { border: 2px solid #ccc; margin: 20px 0; padding: 10px; }
        .test-title { background: #f0f0f0; padding: 5px; margin-bottom: 10px; }
        .width-indicator { background: #ffffcc; padding: 5px; }
    </style>
</head>
<body>
    <h1>Glossary Alignment Test Page</h1>
    
    <div class="test-section">
        <div class="test-title">Content Width Test</div>
        <div class="width-indicator">This yellow bar should extend to the full width of the content area</div>
    </div>
    
    <div class="test-section">
        <div class="test-title">Definition List Test (with CSS applied)</div>
        <section id="common-command-abbreviations">
            <h1>Common Command Abbreviations</h1>
            <dl class="simple glossary">
                <dt id="term-test">Test Term</dt>
                <dd><p>This is a test definition that should be properly aligned and not clipped. The text should wrap normally and use the full width available.</p></dd>
                <dt id="term-another">Another Term</dt>
                <dd><p>Another test definition with longer text to see how it behaves. This text should flow naturally and not be cut off at the edge of the container.</p></dd>
            </dl>
        </section>
    </div>
    
    <div class="test-section">
        <div class="test-title">Plain Text Test</div>
        <p>This is plain paragraph text that should align properly with the left edge and use the full available width. It should not be centered or have any unexpected margins.</p>
    </div>
    
    <script>
        window.onload = function() {
            console.log('Page loaded. Check alignment in browser.');
            
            // Log element widths
            const sections = document.querySelectorAll('.test-section');
            sections.forEach((section, index) => {
                console.log(`Section ${index + 1} width:`, section.offsetWidth + 'px');
            });
            
            const cca = document.getElementById('common-command-abbreviations');
            if (cca) {
                console.log('Common Command Abbreviations width:', cca.offsetWidth + 'px');
                console.log('Common Command Abbreviations left offset:', cca.offsetLeft + 'px');
            }
        };
    </script>
</body>
</html>"""
    
    test_path = "/home/ramesh/Wipro_WILP_Training/docs/alignment_test.html"
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"Created test page: {test_path}")
    return test_path

if __name__ == "__main__":
    print("Testing current glossary structure and alignment...\n")
    test_glossary_structure()
    
    print("\n" + "="*50)
    print("Creating alignment test page...")
    test_path = create_html_test_page()
    print(f"\nOpen {test_path} in a browser to visually verify alignment.")
