#!/usr/bin/env python3
"""
Simple Content Restoration Test
"""

import os
from bs4 import BeautifulSoup

def test_extraction():
    """Test content extraction"""
    
    singlehtml_path = 'singlehtml/index.html'
    
    print("Testing content extraction...")
    
    try:
        with open(singlehtml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for the disk management section
        span = soup.find('span', id='document-disk-management')
        print(f"Found span: {span is not None}")
        
        if span:
            section = span.find_next_sibling('section')
            print(f"Found section after span: {section is not None}")
            
            if section:
                section_text = str(section)[:200]
                print(f"Section preview: {section_text}...")
                
                # Try to restore to disk-management.html
                with open('disk-management.html', 'r', encoding='utf-8') as f:
                    current = f.read()
                
                current_soup = BeautifulSoup(current, 'html.parser')
                rst_content = current_soup.find('div', class_='rst-content')
                print(f"Found rst-content in target: {rst_content is not None}")
                
                if rst_content:
                    breadcrumbs = rst_content.find('div', {'aria-label': 'Page navigation'})
                    print(f"Found breadcrumbs: {breadcrumbs is not None}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_extraction()
