# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

# Data Organization

Understanding Data Organization
------------------------------

Data organization refers to the systematic arrangement and structuring of data to optimize storage efficiency, access speed, and management ease. Proper data organization is crucial for system performance and data integrity.

### Data Organization Fundamentals

#### What is Data Organization?

Data organization encompasses:

* **Data Structure**: How data is arranged and stored
* **Data Classification**: Categorizing data by type, importance, and access patterns
* **Data Hierarchy**: Organizing data in logical levels and relationships
* **Data Access Patterns**: Understanding how data is accessed and used
* **Data Lifecycle**: Managing data from creation to deletion

Data Classification Types
~~~~~~~~~~~~~~~~~~~~~~~~

#### By Access Frequency

1. **Hot Data**: Frequently accessed, requires fast storage (SSD)
2. **Warm Data**: Occasionally accessed, standard performance storage
3. **Cold Data**: Rarely accessed, slower but cost-effective storage
4. **Archival Data**: Long-term retention, very infrequent access

#### By Data Type

1. **Structured Data**: Databases, spreadsheets, organized formats
2. **Semi-structured Data**: JSON, XML, log files
3. **Unstructured Data**: Documents, images, videos, emails

#### By Criticality

1. **Critical Data**: Business-essential, requires high availability
2. **Important Data**: Significant but not critical
3. **Standard Data**: Regular business data
4. **Temporary Data**: Short-term, disposable data

Ubuntu 22.04 Data Organization Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Directory Structure Best Practices

```bash

    # Standard Ubuntu directory structure
    /
    ├── home/           # User data
    ├── var/            # Variable data (logs, databases)
    ├── usr/            # User programs and libraries
    ├── opt/            # Optional software packages
    ├── srv/            # Service data
    ├── tmp/            # Temporary files
    └── mnt/            # Mount points for external storage

    # Recommended user data organization
    /home/username/
    ├── Documents/      # Personal documents
    ├── Projects/       # Development projects
    ├── Media/          # Photos, videos, music
    ├── Archive/        # Old/archived files
    ├── Backup/         # Local backups
    └── Work/           # Work-related files

File Organization Commands
^^^^^^^^^^^^^^^^^^^^^^^^^

```bash

    # Create organized directory structure
    mkdir -p ~/Documents/{Personal,Work}/{2024,2023,Archive}
    mkdir -p ~/Projects/{Active,Completed,Archive}
    mkdir -p ~/Media/{Photos,Videos,Music}/{2024,2023,Archive}

    # File organization by date
    find ~/Downloads -type f -newermt "2024-01-01" ! -newermt "2024-12-31" \
        -exec mkdir -p ~/Archive/2024/ \; -exec mv {} ~/Archive/2024/ \;

    # Organize files by extension
    cd ~/Downloads
    for ext in pdf doc docx txt; do
        mkdir -p ~/Documents/$(echo $ext | tr '[:lower:]' '[:upper:]')
        find . -name "*.$ext" -exec mv {} ~/Documents/$(echo $ext | tr '[:lower:]' '[:upper:]')/ \;
    done

    # Find and organize duplicate files
    fdupes -r ~/Documents -d

### Data Backup and Archival

Backup Strategies
^^^^^^^^^^^^^^^^

```bash

    # 3-2-1 Backup Rule Implementation
    # 3 copies, 2 different media types, 1 offsite

    # Local backup (rsync)
    rsync -avH --delete ~/Documents/ /backup/documents/

    # External drive backup
    rsync -avH --delete ~/Documents/ /media/external/backup/documents/

    # Cloud backup (rclone)
    rclone sync ~/Documents/ cloud:backup/documents/

    # Compressed archive backup
    tar -czf /backup/documents_$(date +%Y%m%d).tar.gz ~/Documents/

#### Automated Data Organization

```bash

    # Create organization script
    cat > ~/bin/organize_data.sh << 'EOF'
    #!/bin/bash
    
    # Organize downloads by file type
    organize_downloads() {
        cd ~/Downloads
        
        # Create directories
        mkdir -p {Documents,Images,Videos,Music,Archives,Software}
        
        # Move files by type
        find . -maxdepth 1 -type f \( -iname "*.pdf" -o -iname "*.doc" -o -iname "*.docx" -o -iname "*.txt" \) -exec mv {} Documents/ \;
        find . -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.jpeg" \) -exec mv {} Images/ \;
        find . -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" \) -exec mv {} Videos/ \;
        find . -maxdepth 1 -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" \) -exec mv {} Music/ \;
        find . -maxdepth 1 -type f \( -iname "*.zip" -o -iname "*.tar.gz" -o -iname "*.rar" \) -exec mv {} Archives/ \;
        find . -maxdepth 1 -type f \( -iname "*.deb" -o -iname "*.appimage" \) -exec mv {} Software/ \;
    }
    
    # Clean old temporary files
    clean_temp() {
        find ~/Downloads -type f -mtime +30 -delete
        find ~/.cache -type f -mtime +7 -delete
        find /tmp -user $USER -type f -mtime +1 -delete 2>/dev/null
    }
    
    # Archive old files
    archive_old() {
        find ~/Documents -type f -mtime +365 -exec mkdir -p ~/Archive/$(date +%Y) \; -exec mv {} ~/Archive/$(date +%Y)/ \;
    }
    
    # Execute functions
    organize_downloads
    clean_temp
    archive_old
    
    echo "Data organization completed: $(date)"
    EOF
    
    chmod +x ~/bin/organize_data.sh
    
    # Schedule with cron
    echo "0 2 * * * ~/bin/organize_data.sh" | crontab -

Data Compression and Deduplication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### File Compression Techniques

```bash

    # Install compression tools
    sudo apt install p7zip-full rar unrar gzip bzip2 xz-utils

    # Create compressed archives
    # gzip (fast, good compression)
    tar -czf archive.tar.gz /path/to/data

    # bzip2 (better compression, slower)
    tar -cjf archive.tar.bz2 /path/to/data

    # xz (best compression, slowest)
    tar -cJf archive.tar.xz /path/to/data

    # 7zip (excellent compression)
    7z a -t7z -mx=9 archive.7z /path/to/data

    # Compare compression ratios
    for method in gz bz2 xz 7z; do
        echo "Compressing with $method..."
        case $method in
            gz) tar -czf test.tar.gz ~/Documents ;;
            bz2) tar -cjf test.tar.bz2 ~/Documents ;;
            xz) tar -cJf test.tar.xz ~/Documents ;;
            7z) 7z a test.7z ~/Documents ;;
        esac
        echo "$method: $(ls -lh test.*$method* | awk '{print $5}')"
    done

#### Duplicate File Management

```bash

    # Install deduplication tools
    sudo apt install fdupes rdfind

    # Find duplicates with fdupes
    fdupes -r ~/Documents

    # Find and delete duplicates interactively
    fdupes -r -d ~/Documents

    # Find duplicates with rdfind
    rdfind ~/Documents

    # Advanced duplicate handling with rdfind
    rdfind -makehardlinks true ~/Documents
    rdfind -makeresultsfile false -makehardlinks true ~/Documents

Data Monitoring and Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Storage Usage Analysis
^^^^^^^^^^^^^^^^^^^^^

```bash

    # Analyze disk usage by directory
    ncdu /home

    # Find largest files
    find /home -type f -exec du -h {} + | sort -rh | head -20

    # Analyze file types and sizes
    find /home -type f | sed 's/.*\\.//' | sort | uniq -c | sort -rn

    # Monitor storage usage trends
    cat > ~/bin/storage_trend.sh << 'EOF'
    #!/bin/bash
    
    LOGFILE="/var/log/storage_usage.log"
    
    echo "$(date): $(df -h / | tail -1 | awk '{print $5}')" >> $LOGFILE
    
    # Generate weekly report
    if [ "$(date +%u)" -eq 1 ]; then
        echo "Weekly Storage Report - $(date)" > /tmp/storage_report.txt
        tail -7 $LOGFILE >> /tmp/storage_report.txt
        mail -s "Storage Usage Report" admin@example.com < /tmp/storage_report.txt
    fi
    EOF
    
    chmod +x ~/bin/storage_trend.sh
    echo "0 0 * * * ~/bin/storage_trend.sh" | crontab -

File System Metadata Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```bash

    # Analyze inode usage
    df -i

    # Find directories with most files
    find /home -type d -exec sh -c 'echo "$(find "$1" -maxdepth 1 | wc -l) $1"' _ {} \; | sort -rn | head -10

    # Analyze file access patterns
    find /home -type f -atime -7 | wc -l  # Files accessed in last 7 days
    find /home -type f -mtime -7 | wc -l  # Files modified in last 7 days
    find /home -type f -atime +365 | wc -l  # Files not accessed in over a year

Frequently Asked Questions
~~~~~~~~~~~~~~~~~~~~~~~~~

Q: How should I organize my home directory in Ubuntu 22.04?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**A:** Follow this recommended structure:

```bash

    ~/
    ├── Documents/
    │   ├── Personal/
    │   ├── Work/
    │   └── Archive/
    ├── Projects/
    │   ├── Active/
    │   ├── Completed/
    │   └── Learning/
    ├── Media/
    │   ├── Photos/
    │   ├── Videos/
    │   └── Music/
    ├── Downloads/
    │   └── (temporary, clean regularly)
    ├── Backup/
    │   └── (local backup copies)
    └── Scripts/
        └── (personal automation scripts)

#### Q: What's the best way to handle duplicate files?

**A:** Use these strategies:

```bash

    # 1. Find duplicates without deleting
    fdupes -r ~/Documents

    # 2. Interactive deletion
    fdupes -r -d ~/Documents

    # 3. Automatic deletion (keep first occurrence)
    fdupes -r -f ~/Documents | grep -v '^$' | xargs rm

    # 4. Convert to hard links (saves space)
    rdfind -makehardlinks true ~/Documents

Q: How can I automate file organization?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**A:** Create automated organization scripts:

```bash

    # File organizer by extension
    #!/bin/bash
    organize_by_extension() {
        local source_dir="$1"
        local target_dir="$2"
        
        cd "$source_dir"
        
        for file in *.*; do
            if [ -f "$file" ]; then
                ext="${file##*.}"
                ext_upper=$(echo "$ext" | tr '[:lower:]' '[:upper:]')
                mkdir -p "$target_dir/$ext_upper"
                mv "$file" "$target_dir/$ext_upper/"
            fi
        done
    }
    
    # Usage
    organize_by_extension ~/Downloads ~/Downloads/Organized

Q: How do I implement a data retention policy?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**A:** Create a retention management system:

```bash

    #!/bin/bash
    # data_retention.sh
    
    # Define retention periods (days)
    TEMP_RETENTION=7
    LOG_RETENTION=90
    BACKUP_RETENTION=365
    ARCHIVE_RETENTION=2555  # 7 years
    
    # Clean temporary files
    find /tmp -type f -mtime +$TEMP_RETENTION -delete
    find ~/.cache -type f -mtime +$TEMP_RETENTION -delete
    
    # Archive old logs
    find /var/log -name "*.log" -mtime +$LOG_RETENTION -gzip
    
    # Remove old backups
    find /backup -name "*.tar.gz" -mtime +$BACKUP_RETENTION -delete
    
    # Alert for very old archives
    find /archive -type f -mtime +$ARCHIVE_RETENTION -ls | \
        mail -s "Files exceeding retention policy" admin@example.com

### Coding Examples

#### Python Data Organization Manager

```python

    #!/usr/bin/env python3
    """
    Advanced data organization manager for Ubuntu 22.04
    """
    import os
    import shutil
    import hashlib
    import json
    import time
    import mimetypes
    from pathlib import Path
    from collections import defaultdict
    import argparse

    class DataOrganizer:
        def __init__(self, base_path=None):
            self.base_path = Path(base_path) if base_path else Path.home()
            self.file_types = {
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
                'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'music': ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac'],
                'archives': ['.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z'],
                'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
                'data': ['.csv', '.json', '.xml', '.sql', '.db', '.sqlite']
            }
            self.stats = defaultdict(int)

        def get_file_hash(self, filepath):
            """Calculate MD5 hash of a file"""
            hash_md5 = hashlib.md5()
            try:
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
            except (IOError, OSError):
                return None

        def find_duplicates(self, directory):
            """Find duplicate files in a directory"""
            duplicates = defaultdict(list)
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = Path(root) / file
                    if filepath.is_file():
                        file_hash = self.get_file_hash(filepath)
                        if file_hash:
                            duplicates[file_hash].append(filepath)
            
            # Filter out unique files
            return {k: v for k, v in duplicates.items() if len(v) > 1}

        def organize_by_type(self, source_dir, target_dir=None):
            """Organize files by type"""
            source_path = Path(source_dir)
            target_path = Path(target_dir) if target_dir else source_path / "Organized"
            
            if not source_path.exists():
                raise ValueError(f"Source directory {source_path} does not exist")
            
            target_path.mkdir(exist_ok=True)
            
            for file_path in source_path.rglob('*'):
                if file_path.is_file() and file_path.parent == source_path:
                    file_ext = file_path.suffix.lower()
                    
                    # Determine file category
                    category = 'misc'
                    for cat, extensions in self.file_types.items():
                        if file_ext in extensions:
                            category = cat
                            break
                    
                    # Create category directory
                    category_dir = target_path / category.title()
                    category_dir.mkdir(exist_ok=True)
                    
                    # Move file
                    new_path = category_dir / file_path.name
                    
                    # Handle naming conflicts
                    counter = 1
                    original_name = new_path.stem
                    while new_path.exists():
                        new_path = category_dir / f"{original_name}_{counter}{file_path.suffix}"
                        counter += 1
                    
                    try:
                        shutil.move(str(file_path), str(new_path))
                        self.stats[f'moved_{category}'] += 1
                        print(f"Moved {file_path.name} to {category.title()}/")
                    except (IOError, OSError) as e:
                        print(f"Error moving {file_path}: {e}")

        def organize_by_date(self, source_dir, target_dir=None):
            """Organize files by modification date"""
            source_path = Path(source_dir)
            target_path = Path(target_dir) if target_dir else source_path / "ByDate"
            
            target_path.mkdir(exist_ok=True)
            
            for file_path in source_path.rglob('*'):
                if file_path.is_file():
                    # Get modification time
                    mtime = file_path.stat().st_mtime
                    date_str = time.strftime('%Y/%m', time.localtime(mtime))
                    
                    # Create date directory
                    date_dir = target_path / date_str
                    date_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    new_path = date_dir / file_path.name
                    
                    # Handle naming conflicts
                    counter = 1
                    original_name = new_path.stem
                    while new_path.exists():
                        new_path = date_dir / f"{original_name}_{counter}{file_path.suffix}"
                        counter += 1
                    
                    try:
                        shutil.move(str(file_path), str(new_path))
                        self.stats['moved_by_date'] += 1
                    except (IOError, OSError) as e:
                        print(f"Error moving {file_path}: {e}")

        def clean_empty_directories(self, directory):
            """Remove empty directories"""
            removed_count = 0
            for root, dirs, files in os.walk(directory, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            removed_count += 1
                            print(f"Removed empty directory: {dir_path}")
                    except OSError:
                        pass  # Directory not empty or permission denied
            
            self.stats['removed_empty_dirs'] = removed_count

        def analyze_directory(self, directory):
            """Analyze directory structure and file distribution"""
            analysis = {
                'total_files': 0,
                'total_size': 0,
                'file_types': defaultdict(int),
                'size_by_type': defaultdict(int),
                'largest_files': [],
                'oldest_files': [],
                'newest_files': []
            }
            
            files_with_info = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.is_file():
                        try:
                            stat_info = file_path.stat()
                            file_size = stat_info.st_size
                            file_ext = file_path.suffix.lower()
                            
                            analysis['total_files'] += 1
                            analysis['total_size'] += file_size
                            analysis['file_types'][file_ext] += 1
                            analysis['size_by_type'][file_ext] += file_size
                            
                            files_with_info.append({
                                'path': file_path,
                                'size': file_size,
                                'mtime': stat_info.st_mtime
                            })
                        except OSError:
                            continue
            
            # Sort files for top lists
            files_with_info.sort(key=lambda x: x['size'], reverse=True)
            analysis['largest_files'] = [
                {'path': str(f['path']), 'size_mb': f['size'] / (1024*1024)}
                for f in files_with_info[:10]
            ]
            
            files_with_info.sort(key=lambda x: x['mtime'])
            analysis['oldest_files'] = [
                {'path': str(f['path']), 'date': time.strftime('%Y-%m-%d', time.localtime(f['mtime']))}
                for f in files_with_info[:10]
            ]
            
            files_with_info.sort(key=lambda x: x['mtime'], reverse=True)
            analysis['newest_files'] = [
                {'path': str(f['path']), 'date': time.strftime('%Y-%m-%d', time.localtime(f['mtime']))}
                for f in files_with_info[:10]
            ]
            
            return analysis

        def create_backup_structure(self, source_dir, backup_dir):
            """Create organized backup structure"""
            source_path = Path(source_dir)
            backup_path = Path(backup_dir)
            
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            backup_target = backup_path / f"backup_{timestamp}"
            backup_target.mkdir(parents=True, exist_ok=True)
            
            # Copy files with organization
            for category, extensions in self.file_types.items():
                category_backup = backup_target / category
                category_backup.mkdir(exist_ok=True)
                
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = Path(root) / file
                        if file_path.suffix.lower() in extensions:
                            try:
                                shutil.copy2(file_path, category_backup)
                                self.stats[f'backed_up_{category}'] += 1
                            except (IOError, OSError) as e:
                                print(f"Error backing up {file_path}: {e}")

        def generate_report(self):
            """Generate organization report"""
            report = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'statistics': dict(self.stats),
                'summary': f"Processed {sum(self.stats.values())} operations"
            }
            
            return json.dumps(report, indent=2)

    def main():
        parser = argparse.ArgumentParser(description='Data Organization Manager')
        parser.add_argument('command', choices=['organize', 'analyze', 'duplicates', 'backup', 'clean'])
        parser.add_argument('source', help='Source directory')
        parser.add_argument('--target', help='Target directory')
        parser.add_argument('--by-type', action='store_true', help='Organize by file type')
        parser.add_argument('--by-date', action='store_true', help='Organize by date')
        
        args = parser.parse_args()
        
        organizer = DataOrganizer()
        
        if args.command == 'organize':
            if args.by_type:
                organizer.organize_by_type(args.source, args.target)
            elif args.by_date:
                organizer.organize_by_date(args.source, args.target)
            else:
                organizer.organize_by_type(args.source, args.target)
                
        elif args.command == 'analyze':
            analysis = organizer.analyze_directory(args.source)
            print(json.dumps(analysis, indent=2, default=str))
            
        elif args.command == 'duplicates':
            duplicates = organizer.find_duplicates(args.source)
            print(f"Found {len(duplicates)} sets of duplicate files:")
            for hash_val, files in duplicates.items():
                print(f"Hash {hash_val[:8]}...")
                for file in files:
                    print(f"  {file}")
                    
        elif args.command == 'backup':
            if not args.target:
                print("Target directory required for backup")
                return
            organizer.create_backup_structure(args.source, args.target)
            
        elif args.command == 'clean':
            organizer.clean_empty_directories(args.source)
        
        print(organizer.generate_report())

    if __name__ == "__main__":
        main()

Bash File Organization System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```bash

    #!/bin/bash
    # advanced_file_organizer.sh - Advanced file organization system for Ubuntu 22.04

    # Configuration
    CONFIG_FILE="$HOME/.file_organizer.conf"
    LOG_FILE="$HOME/.file_organizer.log"

    # Default configuration
    cat > "$CONFIG_FILE" << 'EOF'
    # File Organization Configuration
    ORGANIZE_DOWNLOADS=true
    ORGANIZE_DESKTOP=true
    AUTO_ARCHIVE_DAYS=365
    DUPLICATE_ACTION=ask  # ask, delete, link
    BACKUP_ENABLED=true
    BACKUP_DIR="$HOME/Backup"
    
    # File type definitions
    DOCUMENTS="pdf doc docx txt rtf odt"
    IMAGES="jpg jpeg png gif bmp tiff svg"
    VIDEOS="mp4 avi mkv mov wmv flv webm"
    MUSIC="mp3 flac wav ogg m4a aac"
    ARCHIVES="zip tar gz bz2 xz rar 7z"
    CODE="py js html css java cpp c php"
    DATA="csv json xml sql db sqlite"
    EOF

    # Load configuration
    source "$CONFIG_FILE"

    # Logging function
    log_message() {
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
        echo "$1"
    }

    # Create directory structure
    create_structure() {
        local base_dir="$1"
        
        log_message "Creating directory structure in $base_dir"
        
        mkdir -p "$base_dir"/{Documents,Images,Videos,Music,Archives,Code,Data,Misc}
        mkdir -p "$base_dir"/Archive/{$(date +%Y),$(date -d 'last year' +%Y)}
        mkdir -p "$base_dir"/Backup
        
        log_message "Directory structure created"
    }

    # Get file category
    get_file_category() {
        local file="$1"
        local extension="${file##*.}"
        extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
        
        case " $DOCUMENTS " in *" $extension "*) echo "Documents"; return ;; esac
        case " $IMAGES " in *" $extension "*) echo "Images"; return ;; esac
        case " $VIDEOS " in *" $extension "*) echo "Videos"; return ;; esac
        case " $MUSIC " in *" $extension "*) echo "Music"; return ;; esac
        case " $ARCHIVES " in *" $extension "*) echo "Archives"; return ;; esac
        case " $CODE " in *" $extension "*) echo "Code"; return ;; esac
        case " $DATA " in *" $extension "*) echo "Data"; return ;; esac
        
        echo "Misc"
    }

    # Organize files by type
    organize_by_type() {
        local source_dir="$1"
        local target_dir="$2"
        
        log_message "Organizing files from $source_dir to $target_dir"
        
        create_structure "$target_dir"
        
        local moved_count=0
        
        find "$source_dir" -maxdepth 1 -type f | while read -r file; do
            if [[ -f "$file" ]]; then
                local filename=$(basename "$file")
                local category=$(get_file_category "$filename")
                local target_file="$target_dir/$category/$filename"
                
                # Handle name conflicts
                local counter=1
                local base_name="${filename%.*}"
                local extension="${filename##*.}"
                
                while [[ -e "$target_file" ]]; do
                    if [[ "$extension" != "$filename" ]]; then
                        target_file="$target_dir/$category/${base_name}_${counter}.${extension}"
                    else
                        target_file="$target_dir/$category/${filename}_${counter}"
                    fi
                    ((counter++))
                done
                
                if mv "$file" "$target_file"; then
                    log_message "Moved $filename to $category/"
                    ((moved_count++))
                else
                    log_message "Failed to move $filename"
                fi
            fi
        done
        
        log_message "Organized $moved_count files"
    }

    # Find and handle duplicates
    handle_duplicates() {
        local directory="$1"
        local action="${2:-$DUPLICATE_ACTION}"
        
        log_message "Finding duplicates in $directory"
        
        if ! command -v fdupes &> /dev/null; then
            log_message "Installing fdupes for duplicate detection"
            sudo apt update && sudo apt install -y fdupes
        fi
        
        local duplicates_file="/tmp/duplicates_$$"
        fdupes -r "$directory" > "$duplicates_file"
        
        local duplicate_sets=0
        local files_processed=0
        
        while IFS= read -r line; do
            if [[ -z "$line" ]]; then
                ((duplicate_sets++))
            elif [[ -f "$line" ]]; then
                case "$action" in
                    "delete")
                        if [[ $files_processed -gt 0 ]]; then
                            rm "$line"
                            log_message "Deleted duplicate: $line"
                        fi
                        ;;
                    "link")
                        if [[ $files_processed -gt 0 ]]; then
                            local first_file=$(head -1 "$duplicates_file")
                            rm "$line"
                            ln "$first_file" "$line"
                            log_message "Linked duplicate: $line"
                        fi
                        ;;
                    "ask")
                        if [[ $files_processed -gt 0 ]]; then
                            echo "Duplicate found: $line"
                            read -p "Delete this file? (y/N): " -n 1 -r
                            echo
                            if [[ $REPLY =~ ^[Yy]$ ]]; then
                                rm "$line"
                                log_message "User deleted duplicate: $line"
                            fi
                        fi
                        ;;
                esac
                ((files_processed++))
            fi
        done < "$duplicates_file"
        
        rm "$duplicates_file"
        log_message "Processed $duplicate_sets sets of duplicates"
    }

    # Archive old files
    archive_old_files() {
        local source_dir="$1"
        local days="${2:-$AUTO_ARCHIVE_DAYS}"
        
        log_message "Archiving files older than $days days from $source_dir"
        
        local archive_dir="$source_dir/Archive/$(date +%Y)"
        mkdir -p "$archive_dir"
        
        local archived_count=0
        
        find "$source_dir" -type f -mtime +$days ! -path "*/Archive/*" ! -path "*/Backup/*" | while read -r file; do
            local relative_path="${file#$source_dir/}"
            local archive_path="$archive_dir/$relative_path"
            local archive_parent=$(dirname "$archive_path")
            
            mkdir -p "$archive_parent"
            
            if mv "$file" "$archive_path"; then
                log_message "Archived: $relative_path"
                ((archived_count++))
            fi
        done
        
        log_message "Archived $archived_count files"
    }

    # Create backup
    create_backup() {
        local source_dir="$1"
        local backup_dir="${2:-$BACKUP_DIR}"
        
        if [[ "$BACKUP_ENABLED" != "true" ]]; then
            log_message "Backup disabled in configuration"
            return
        fi
        
        log_message "Creating backup of $source_dir to $backup_dir"
        
        local timestamp=$(date +%Y%m%d_%H%M%S)
        local backup_target="$backup_dir/backup_$timestamp"
        
        mkdir -p "$backup_target"
        
        if rsync -av --progress "$source_dir/" "$backup_target/"; then
            log_message "Backup created successfully: $backup_target"
            
            # Compress backup
            if command -v tar &> /dev/null; then
                tar -czf "$backup_target.tar.gz" -C "$backup_dir" "backup_$timestamp"
                rm -rf "$backup_target"
                log_message "Backup compressed: $backup_target.tar.gz"
            fi
        else
            log_message "Backup failed"
        fi
    }

    # Generate organization report
    generate_report() {
        local directory="$1"
        local report_file="/tmp/organization_report_$(date +%Y%m%d).txt"
        
        {
            echo "File Organization Report"
            echo "========================"
            echo "Generated: $(date)"
            echo "Directory: $directory"
            echo ""
            
            echo "Directory Structure:"
            tree -d -L 2 "$directory" 2>/dev/null || find "$directory" -type d | head -20
            echo ""
            
            echo "File Count by Type:"
            for type in Documents Images Videos Music Archives Code Data Misc; do
                if [[ -d "$directory/$type" ]]; then
                    count=$(find "$directory/$type" -type f | wc -l)
                    echo "$type: $count files"
                fi
            done
            echo ""
            
            echo "Storage Usage:"
            du -sh "$directory"/* 2>/dev/null | sort -hr
            echo ""
            
            echo "Recent Activity (from log):"
            tail -20 "$LOG_FILE"
            
        } > "$report_file"
        
        echo "Report generated: $report_file"
        
        # Email report if mail is configured
        if command -v mail &> /dev/null; then
            cat "$report_file" | mail -s "File Organization Report" "$USER@localhost"
        fi
    }

    # Main execution
    main() {
        case "${1:-help}" in
            "organize")
                organize_by_type "${2:-$HOME/Downloads}" "${3:-$HOME/Organized}"
                ;;
            "duplicates")
                handle_duplicates "${2:-$HOME}" "${3:-ask}"
                ;;
            "archive")
                archive_old_files "${2:-$HOME}" "${3:-365}"
                ;;
            "backup")
                create_backup "${2:-$HOME}" "${3:-$BACKUP_DIR}"
                ;;
            "report")
                generate_report "${2:-$HOME}"
                ;;
            "full")
                # Full organization workflow
                local target_dir="${2:-$HOME/Organized}"
                
                log_message "Starting full organization workflow"
                
                create_backup "$HOME/Downloads"
                organize_by_type "$HOME/Downloads" "$target_dir"
                handle_duplicates "$target_dir" "ask"
                archive_old_files "$target_dir"
                generate_report "$target_dir"
                
                log_message "Full organization workflow completed"
                ;;
            "config")
                nano "$CONFIG_FILE"
                ;;
            "help"|*)
                echo "Advanced File Organizer for Ubuntu 22.04"
                echo "Usage: $0 [command] [options]"
                echo ""
                echo "Commands:"
                echo "  organize [source] [target]    - Organize files by type"
                echo "  duplicates [dir] [action]     - Handle duplicate files (ask/delete/link)"
                echo "  archive [dir] [days]          - Archive old files"
                echo "  backup [source] [target]      - Create backup"
                echo "  report [directory]            - Generate organization report"
                echo "  full [target]                 - Run complete organization workflow"
                echo "  config                        - Edit configuration"
                echo ""
                echo "Examples:"
                echo "  $0 organize ~/Downloads ~/Organized"
                echo "  $0 duplicates ~/Documents delete"
                echo "  $0 archive ~/Documents 180"
                echo "  $0 full ~/MyFiles"
                ;;
        esac
    }

    # Run main function with all arguments
    main "$@"

Best Practices for Data Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Strategic Planning

1. **Data Classification Strategy**:
   
   * Identify data types and access patterns
   * Define retention policies
   * Establish backup requirements
   * Plan for data growth

2. **Directory Structure Design**:
   
   * Use consistent naming conventions
   * Implement logical hierarchies
   * Plan for scalability
   * Document organization rules

#### Automation and Maintenance

1. **Automated Organization**:
   
   ```bash

       # Daily organization cron job
       0 2 * * * /home/user/bin/organize_data.sh

       # Weekly duplicate cleanup
       0 1 * * 0 fdupes -r -d /home/user/Documents

       # Monthly archival
       0 0 1 * * /home/user/bin/archive_old_files.sh

2. **Monitoring and Alerts**:
   
   ```bash

       # Storage usage monitoring
       if [ $(df / | tail -1 | awk '{print $5}' | sed 's/%//') -gt 85 ]; then
           echo "Disk usage critical" | mail -s "Storage Alert" admin
       fi

Security and Compliance
^^^^^^^^^^^^^^^^^^^^^^

1. **Data Protection**:
   
   * Implement access controls
   * Use encryption for sensitive data
   * Regular security audits
   * Backup verification

2. **Compliance Requirements**:
   
   * Document data handling procedures
   * Implement retention policies
   * Audit trail maintenance
   * Regular compliance reviews

```bash

    # Set up secure data handling
    # Encrypt sensitive directories
    sudo apt install ecryptfs-utils
    ecryptfs-migrate-home -u username

    # Set appropriate permissions
    find /home/user/Documents -type f -exec chmod 640 {} \;
    find /home/user/Documents -type d -exec chmod 750 {} \;

```

---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---