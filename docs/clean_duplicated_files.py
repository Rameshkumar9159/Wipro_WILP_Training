#!/usr/bin/env python3
"""
HTML Deduplication Script
Fixes files that have been corrupted with duplicate content
"""

import os
import re
from bs4 import BeautifulSoup

def clean_html_file(file_path):
    """Clean duplicated content from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the first complete HTML structure
        first_html = soup.find('html')
        if not first_html:
            print(f"  ⚠️  No HTML structure found in {file_path}")
            return False
        
        # Get the clean HTML content
        clean_content = str(first_html)
        
        # Ensure proper DOCTYPE
        if not clean_content.startswith('<!DOCTYPE'):
            clean_content = '<!DOCTYPE html>\n' + clean_content
        
        # Write the cleaned content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error cleaning {file_path}: {e}")
        return False

def restore_from_backup_if_needed():
    """Check if we need to restore from any backup files"""
    backup_files = [f for f in os.listdir('.') if f.endswith('.bak')]
    if backup_files:
        print(f"Found {len(backup_files)} backup files that could be used for restoration")
        return backup_files
    return []

def main():
    print("=== HTML File Deduplication ===")
    
    # Get all HTML files and their sizes
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # Normal expected sizes (approximate)
    normal_sizes = {
        'search.html': 200,
        'storage-overview.html': 600,
        'genindex.html': 600, 
        'index.html': 600,
        'storage-devices.html': 1000,
        'coding-examples.html': 1500,
        'glossary.html': 1600
    }
    
    corrupted_files = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r') as f:
                line_count = sum(1 for _ in f)
            
            # If file is suspiciously large, it's likely corrupted
            if line_count > 2000:  # Most normal files should be under 2000 lines
                corrupted_files.append((html_file, line_count))
                print(f"🔍 {html_file}: {line_count} lines (SUSPECTED CORRUPTION)")
            else:
                print(f"✅ {html_file}: {line_count} lines (OK)")
        except:
            print(f"❌ {html_file}: Could not read")
    
    if not corrupted_files:
        print("\n✅ No corrupted files detected!")
        return
    
    print(f"\n🛠️  Found {len(corrupted_files)} corrupted files to clean:")
    
    for file_path, line_count in corrupted_files:
        print(f"\nCleaning {file_path} ({line_count} lines)...")
        
        # Create backup first
        backup_path = f"{file_path}.backup"
        try:
            with open(file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"  📁 Backup created: {backup_path}")
        except:
            print(f"  ⚠️  Could not create backup for {file_path}")
        
        # Clean the file
        if clean_html_file(file_path):
            # Check new size
            try:
                with open(file_path, 'r') as f:
                    new_line_count = sum(1 for _ in f)
                print(f"  ✅ Cleaned: {line_count} → {new_line_count} lines")
            except:
                print(f"  ✅ File cleaned successfully")
        else:
            print(f"  ❌ Failed to clean {file_path}")
    
    print(f"\n=== SUMMARY ===")
    print(f"✅ Processed {len(corrupted_files)} corrupted files")
    print("🔧 Navigation should now work properly without UI issues")
    print("📁 Backup files created for safety")

if __name__ == "__main__":
    main()
