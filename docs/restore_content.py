#!/usr/bin/env python3
"""
Restore Content from Backup Files
Extract the actual content from backup files while preserving navigation fixes
"""

import os
import re
from bs4 import BeautifulSoup

def extract_content_from_backup(backup_file):
    """Extract main content from backup file"""
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the main content area
        main_content = soup.find('div', class_='rst-content')
        if main_content:
            # Extract the main content div
            main_div = main_content.find('div', {'itemprop': 'articleBody'})
            if main_div:
                return str(main_div)
            else:
                # Try to find article content
                article = main_content.find('article')
                if article:
                    return str(article)
                else:
                    # Return the entire rst-content if no specific article found
                    return str(main_content)
        
        # If no rst-content found, try to find document content
        document = soup.find('div', class_='document')
        if document:
            return str(document)
        
        return None
    
    except Exception as e:
        print(f"Error extracting content from {backup_file}: {e}")
        return None

def restore_content_to_file(html_file, backup_file):
    """Restore content from backup to current file while preserving navigation"""
    try:
        # Read current file (has correct navigation structure)
        with open(html_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Extract content from backup
        backup_content = extract_content_from_backup(backup_file)
        if not backup_content:
            print(f"Could not extract content from {backup_file}")
            return False
        
        # Parse current file
        soup = BeautifulSoup(current_content, 'html.parser')
        
        # Find where to insert content (after breadcrumbs)
        content_area = soup.find('div', class_='rst-content')
        if content_area:
            # Clear any existing malformed content
            existing_main = content_area.find('div', {'itemprop': 'articleBody'})
            if existing_main:
                existing_main.decompose()
            
            # Parse and insert backup content
            backup_soup = BeautifulSoup(backup_content, 'html.parser')
            
            # Find the navigation (breadcrumbs) area to insert after
            breadcrumbs = content_area.find('div', {'aria-label': 'Page navigation'})
            if breadcrumbs:
                # Insert content after breadcrumbs
                for element in backup_soup.children:
                    if element.name:  # Skip text nodes
                        breadcrumbs.insert_after(element)
                        breadcrumbs = element  # Update position for next insertion
            else:
                # If no breadcrumbs found, append to content area
                content_area.append(backup_soup)
        
        # Save updated file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error restoring content to {html_file}: {e}")
        return False

def main():
    print("=== Content Restoration from Backups ===")
    
    # Get all backup files
    backup_files = [f for f in os.listdir('.') if f.endswith('.backup')]
    backup_files.sort()
    
    restored_count = 0
    
    for backup_file in backup_files:
        html_file = backup_file.replace('.backup', '')
        
        if os.path.exists(html_file):
            print(f"Restoring content: {backup_file} → {html_file}")
            
            if restore_content_to_file(html_file, backup_file):
                print(f"  ✅ Content restored to {html_file}")
                restored_count += 1
            else:
                print(f"  ❌ Failed to restore content to {html_file}")
        else:
            print(f"  ⚠️  Target file {html_file} not found for {backup_file}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Content restored to {restored_count} files")
    
    # Check file sizes after restoration
    print("\nFile sizes after content restoration:")
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for html_file in sorted(html_files):
        size_kb = os.path.getsize(html_file) / 1024
        print(f"  {html_file}: {size_kb:.1f}KB")

if __name__ == "__main__":
    main()
