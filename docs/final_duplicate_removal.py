#!/usr/bin/env python3
"""
Final duplicate removal script for glossary.html
Author: T S Rameshkumar
Batch: WiproNGA_Datacentre_B9_25VID2182
Purpose: Remove remaining duplicate sections in glossary.html that are causing alignment issues
"""

import re
import os

def remove_duplicate_sections():
    """Remove duplicate sections from glossary.html"""
    
    glossary_path = "/home/ramesh/Wipro_WILP_Training/docs/glossary.html"
    
    if not os.path.exists(glossary_path):
        print(f"Error: {glossary_path} not found")
        return False
    
    print("Reading glossary.html...")
    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_path = glossary_path + '.backup_before_final_dedup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created backup: {backup_path}")
    
    # Find all section start positions
    section_pattern = r'<section id="([^"]+)">'
    sections_found = []
    
    for match in re.finditer(section_pattern, content):
        section_id = match.group(1)
        start_pos = match.start()
        sections_found.append((section_id, start_pos, match.group(0)))
    
    print(f"Found {len(sections_found)} sections:")
    for section_id, pos, tag in sections_found:
        print(f"  - {section_id} at position {pos}")
    
    # Track which sections we've seen
    seen_sections = set()
    sections_to_remove = []
    
    for section_id, start_pos, tag in sections_found:
        if section_id in seen_sections:
            print(f"Duplicate found: {section_id} at position {start_pos}")
            sections_to_remove.append((section_id, start_pos))
        else:
            seen_sections.add(section_id)
    
    if not sections_to_remove:
        print("No duplicate sections found!")
        return True
    
    print(f"\nWill remove {len(sections_to_remove)} duplicate sections:")
    for section_id, pos in sections_to_remove:
        print(f"  - {section_id} at position {pos}")
    
    # Remove duplicates starting from the end to preserve positions
    sections_to_remove.sort(key=lambda x: x[1], reverse=True)
    
    for section_id, start_pos in sections_to_remove:
        print(f"\nRemoving duplicate section: {section_id}")
        
        # Find the start of this section
        section_start_pattern = f'<section id="{re.escape(section_id)}">'
        section_start_match = re.search(section_start_pattern, content[start_pos:])
        
        if not section_start_match:
            print(f"Warning: Could not find section start for {section_id}")
            continue
        
        actual_start = start_pos + section_start_match.start()
        
        # Find the end of this section (next section or end of content)
        remaining_content = content[actual_start:]
        
        # Look for the closing </section> tag that matches this section
        section_depth = 0
        pos = 0
        section_end = None
        
        while pos < len(remaining_content):
            # Look for section tags
            next_section_start = remaining_content.find('<section', pos)
            next_section_end = remaining_content.find('</section>', pos)
            
            if next_section_start != -1 and (next_section_end == -1 or next_section_start < next_section_end):
                # Found a section start
                section_depth += 1
                pos = next_section_start + 8  # len('<section')
            elif next_section_end != -1:
                # Found a section end
                if section_depth == 1:
                    # This is the end of our section
                    section_end = actual_start + next_section_end + 10  # len('</section>')
                    break
                else:
                    section_depth -= 1
                    pos = next_section_end + 10
            else:
                # No more section tags found
                break
        
        if section_end is None:
            print(f"Warning: Could not find end of section {section_id}")
            continue
        
        # Remove the section
        print(f"Removing content from position {actual_start} to {section_end}")
        content = content[:actual_start] + content[section_end:]
        print(f"Section {section_id} removed successfully")
    
    # Write the cleaned content
    with open(glossary_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nCleaned glossary.html saved!")
    print(f"Backup available at: {backup_path}")
    
    # Verify no more duplicates
    final_sections = re.findall(section_pattern, content)
    final_unique_sections = set(final_sections)
    
    print(f"\nVerification:")
    print(f"Total sections after cleanup: {len(final_sections)}")
    print(f"Unique sections after cleanup: {len(final_unique_sections)}")
    
    if len(final_sections) == len(final_unique_sections):
        print("✓ No more duplicate sections!")
        return True
    else:
        print("✗ Still have duplicate sections!")
        return False

if __name__ == "__main__":
    print("Starting final duplicate section removal...")
    success = remove_duplicate_sections()
    
    if success:
        print("\n✓ Duplicate removal completed successfully!")
        print("The glossary.html file should now display with proper alignment.")
    else:
        print("\n✗ Some issues occurred during duplicate removal.")
