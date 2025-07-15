#!/usr/bin/env python3
"""
Aggressive HTML Structure Fix
Fix malformed HTML structure with duplicate sections
"""

import os
import re
from bs4 import BeautifulSoup

def fix_html_structure(file_path):
    """Fix malformed HTML structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any trailing malformed tags
        content = re.sub(r'</h1></div></div></div></div></div></section></div></body></html>$', '', content)
        content = re.sub(r'</section></div></body></html>$', '', content)
        
        # Parse with BeautifulSoup for proper structure
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all wy-nav-content-wrap sections
        content_wraps = soup.find_all('section', class_='wy-nav-content-wrap')
        
        if len(content_wraps) > 1:
            print(f"Found {len(content_wraps)} duplicate content wraps in {file_path}")
            
            # Keep only the first one and remove others
            for i in range(1, len(content_wraps)):
                content_wraps[i].decompose()
        
        # Ensure proper HTML structure
        if soup.html:
            # Make sure there's only one body
            bodies = soup.find_all('body')
            if len(bodies) > 1:
                print(f"Multiple bodies found in {file_path}, fixing...")
                # Merge content into first body
                main_body = bodies[0]
                for i in range(1, len(bodies)):
                    # Move children from duplicate body to main body
                    for child in list(bodies[i].children):
                        main_body.append(child)
                    bodies[i].decompose()
        
        # Ensure proper closing tags
        html_str = str(soup)
        
        # Make sure it ends properly
        if not html_str.strip().endswith('</html>'):
            html_str = html_str.rstrip() + '\n</html>'
        
        # Save fixed version
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_str)
        
        return True
    
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    print("=== Aggressive HTML Structure Fix ===")
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    html_files.sort()
    
    fixed_count = 0
    
    for html_file in html_files:
        print(f"Fixing {html_file}...")
        
        if fix_html_structure(html_file):
            print(f"  ✅ {html_file} structure fixed")
            fixed_count += 1
        else:
            print(f"  ❌ Failed to fix {html_file}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
