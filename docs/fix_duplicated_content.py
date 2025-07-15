#!/usr/bin/env python3
"""
Fix Duplicated HTML Content
Remove duplicate content sections from HTML files that got corrupted during navigation fixes
"""

import os
import re
from bs4 import BeautifulSoup

def clean_duplicated_html(file_path):
    """Remove duplicate content sections from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all main content sections
        main_sections = soup.find_all('div', class_='wy-nav-content')
        
        if len(main_sections) > 1:
            print(f"Found {len(main_sections)} duplicate content sections in {file_path}")
            
            # Keep only the first main content section
            for i in range(1, len(main_sections)):
                main_sections[i].decompose()
            
            # Also remove any duplicate document sections
            doc_sections = soup.find_all('div', class_='document')
            if len(doc_sections) > 1:
                print(f"Found {len(doc_sections)} duplicate document sections in {file_path}")
                for i in range(1, len(doc_sections)):
                    doc_sections[i].decompose()
            
            # Remove duplicate body content
            bodies = soup.find_all('body')
            if len(bodies) > 1:
                print(f"Found {len(bodies)} duplicate body sections in {file_path}")
                # This is more complex, need to merge properly
                
            # Save cleaned version
            cleaned_content = str(soup)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            return True
        
        return False
    
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")
        return False

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def main():
    print("=== HTML Content Deduplication ===")
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    # Reference size (storage-overview.html should be clean)
    ref_size = get_file_size_mb('storage-overview.html')
    print(f"Reference file size (storage-overview.html): {ref_size:.1f}MB")
    
    files_cleaned = 0
    
    for html_file in html_files:
        if html_file == 'storage-overview.html':
            continue
            
        file_size = get_file_size_mb(html_file)
        
        # If file is more than 3x the reference size, it's likely duplicated
        if file_size > ref_size * 3:
            print(f"\n🔧 Cleaning {html_file} (size: {file_size:.1f}MB)")
            
            if clean_duplicated_html(html_file):
                new_size = get_file_size_mb(html_file)
                print(f"   Reduced from {file_size:.1f}MB to {new_size:.1f}MB")
                files_cleaned += 1
            else:
                print(f"   No duplicates found in {html_file}")
        else:
            print(f"✅ {html_file} size OK ({file_size:.1f}MB)")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files cleaned: {files_cleaned}")
    print("Checking final sizes...")
    
    # Show final sizes
    for html_file in html_files:
        size = get_file_size_mb(html_file)
        status = "✅" if size < ref_size * 2 else "⚠️"
        print(f"{status} {html_file}: {size:.1f}MB")

if __name__ == "__main__":
    main()
