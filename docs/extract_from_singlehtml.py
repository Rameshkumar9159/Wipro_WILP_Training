#!/usr/bin/env python3
"""
Extract Content from Single HTML
Extract content sections from singlehtml/index.html and restore to individual files
"""

import os
import re
from bs4 import BeautifulSoup

def extract_section_content(singlehtml_path, section_id):
    """Extract a specific section from the single HTML file"""
    try:
        with open(singlehtml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the span with the section ID first
        span = soup.find('span', id=section_id)
        if span:
            # Get the next section element
            section = span.find_next_sibling('section')
            if section:
                return str(section)
        
        # Fallback: Find section directly by ID
        section = soup.find('section', id=section_id.replace('document-', ''))
        if section:
            return str(section)
        
        return None
    
    except Exception as e:
        print(f"Error extracting section {section_id}: {e}")
        return None

def restore_content_to_html(html_file, content_html):
    """Insert content into existing HTML file while preserving navigation"""
    try:
        # Read current file (has correct navigation)
        with open(html_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        soup = BeautifulSoup(current_content, 'html.parser')
        
        # Find the rst-content area
        rst_content = soup.find('div', class_='rst-content')
        if not rst_content:
            print(f"No rst-content found in {html_file}")
            return False
        
        # Find the breadcrumbs area
        breadcrumbs = rst_content.find('div', {'aria-label': 'Page navigation'})
        if not breadcrumbs:
            print(f"No breadcrumbs found in {html_file}")
            return False
        
        # Remove any existing malformed content after breadcrumbs
        next_sibling = breadcrumbs.next_sibling
        while next_sibling:
            temp = next_sibling.next_sibling
            if hasattr(next_sibling, 'decompose'):
                next_sibling.decompose()
            next_sibling = temp
        
        # Parse the content to insert
        content_soup = BeautifulSoup(content_html, 'html.parser')
        
        # Insert the content after breadcrumbs
        breadcrumbs.insert_after(content_soup)
        
        # Save the file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error restoring content to {html_file}: {e}")
        return False

def main():
    print("=== Content Extraction from Single HTML ===")
    
    singlehtml_path = 'singlehtml/index.html'
    
    if not os.path.exists(singlehtml_path):
        print(f"Single HTML file not found: {singlehtml_path}")
        return
    
    # Map of HTML files to their section IDs (using document- prefix)
    content_mapping = {
        'disk-management.html': 'document-disk-management',
        'file-systems.html': 'document-file-systems', 
        'data-organization.html': 'document-data-organization',
        'raid-systems.html': 'document-raid-systems',
        'network-storage.html': 'document-network-storage',
        'volume-management.html': 'document-volume-management',
        'storage-devices.html': 'document-storage-devices',
        'ubuntu-setup.html': 'document-ubuntu-setup',
        'coding-examples.html': 'document-coding-examples',
        'troubleshooting.html': 'document-troubleshooting',
        'best-practices.html': 'document-best-practices',
        'glossary.html': 'document-glossary',
        'faq.html': 'document-faq',
        'downloads.html': 'document-downloads'
    }
    
    restored_count = 0
    
    for html_file, section_id in content_mapping.items():
        if os.path.exists(html_file):
            print(f"Extracting content for {html_file} (section: {section_id})")
            
            # Extract content from single HTML
            content = extract_section_content(singlehtml_path, section_id)
            
            if content:
                # Restore to individual file
                if restore_content_to_html(html_file, content):
                    print(f"  ✅ Content restored to {html_file}")
                    restored_count += 1
                else:
                    print(f"  ❌ Failed to restore content to {html_file}")
            else:
                print(f"  ⚠️  No content found for section {section_id}")
        else:
            print(f"  ⚠️  File {html_file} not found")
    
    print(f"\n=== SUMMARY ===")
    print(f"Content restored to {restored_count} files")
    
    # Show file sizes after restoration
    print("\nFile sizes after content restoration:")
    for html_file in sorted(content_mapping.keys()):
        if os.path.exists(html_file):
            size_kb = os.path.getsize(html_file) / 1024
            print(f"  {html_file}: {size_kb:.1f}KB")

if __name__ == "__main__":
    main()
