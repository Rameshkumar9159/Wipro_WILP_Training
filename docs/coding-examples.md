# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

# Coding Examples and Scripts

This section provides practical coding examples, scripts, and automation tools for storage management on Ubuntu 22.04.

   :local:
   :depth: 2

## Storage Monitoring Scripts

### System Storage Health Monitor

```python

   #!/usr/bin/env python3
   """
   Storage Health Monitor for Ubuntu 22.04
   Monitors disk usage, SMART status, and filesystem health
   """

   import subprocess
   import json
   import sys
   import time
   from datetime import datetime

   class StorageMonitor:
       def __init__(self):
           self.log_file = "/var/log/storage-monitor.log"
       
       def get_disk_usage(self):
           """Get disk usage for all mounted filesystems"""
           try:
               result = subprocess.run(['df', '-h'], capture_output=True, text=True)
               return result.stdout
           except Exception as e:
               return f"Error getting disk usage: {e}"
       
       def check_smart_status(self, device):
           """Check SMART status for a device"""
           try:
               result = subprocess.run(['smartctl', '-H', device], 
                                     capture_output=True, text=True)
               return "PASSED" in result.stdout
           except Exception as e:
               return False
       
       def get_mounted_devices(self):
           """Get list of mounted block devices"""
           try:
               result = subprocess.run(['lsblk', '-J'], capture_output=True, text=True)
               data = json.loads(result.stdout)
               devices = []
               for device in data['blockdevices']:
                   if device.get('mountpoint'):
                       devices.append(device['name'])
               return devices
           except Exception as e:
               return []
       
       def log_status(self, message):
           """Log status message with timestamp"""
           timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_entry = f"[{timestamp}] {message}\n"
           try:
               with open(self.log_file, 'a') as f:
                   f.write(log_entry)
           except Exception as e:
               print(f"Error writing to log: {e}")
       
       def monitor(self):
           """Main monitoring function"""
           print("Storage Health Monitor - Starting...")
           
           # Check disk usage
           usage = self.get_disk_usage()
           print("Disk Usage:")
           print(usage)
           
           # Check SMART status for physical drives
           devices = ['/dev/sda', '/dev/sdb', '/dev/nvme0n1']
           for device in devices:
               try:
                   smart_ok = self.check_smart_status(device)
                   status = "HEALTHY" if smart_ok else "WARNING"
                   message = f"SMART status for {device}: {status}"
                   print(message)
                   self.log_status(message)
               except Exception as e:
                   print(f"Could not check {device}: {e}")
           
           # Alert on high usage
           for line in usage.split('\n')[1:]:
               if line.strip():
                   parts = line.split()
                   if len(parts) >= 5:
                       usage_pct = parts[4].replace('%', '')
                       if usage_pct.isdigit() and int(usage_pct) > 90:
                           alert = f"HIGH USAGE ALERT: {parts[5]} is {usage_pct}% full"
                           print(alert)
                           self.log_status(alert)

   if __name__ == "__main__":
       monitor = StorageMonitor()
       monitor.monitor()

### Automated Backup Script

```bash

   #!/bin/bash
   # Automated Backup Script for Ubuntu 22.04
   # Supports incremental backups with rotation

   set -euo pipefail

   # Configuration
   SOURCE_DIR="${1:-/home}"
   BACKUP_BASE="/backup"
   RETENTION_DAYS=30
   LOG_FILE="/var/log/backup.log"
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="${BACKUP_BASE}/backup_${DATE}"

   # Functions
   log_message() {
       echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
   }

   check_prerequisites() {
       if [[ $EUID -ne 0 ]]; then
           log_message "ERROR: This script must be run as root"
           exit 1
       fi
       
       if ! command -v rsync &> /dev/null; then
           log_message "Installing rsync..."
           apt update && apt install -y rsync
       fi
       
       mkdir -p "$BACKUP_BASE"
   }

   perform_backup() {
       log_message "Starting backup of $SOURCE_DIR to $BACKUP_DIR"
       
       # Find most recent backup for incremental
       LATEST_BACKUP=$(find "$BACKUP_BASE" -maxdepth 1 -type d -name "backup_*" | sort | tail -1)
       
       if [[ -n "$LATEST_BACKUP" && -d "$LATEST_BACKUP" ]]; then
           log_message "Performing incremental backup from $LATEST_BACKUP"
           rsync -av --link-dest="$LATEST_BACKUP" "$SOURCE_DIR/" "$BACKUP_DIR/"
       else
           log_message "Performing full backup"
           rsync -av "$SOURCE_DIR/" "$BACKUP_DIR/"
       fi
       
       # Create backup manifest
       find "$BACKUP_DIR" -type f -exec sha256sum {} \; > "${BACKUP_DIR}/manifest.sha256"
       echo "Backup completed: $(date)" > "${BACKUP_DIR}/backup_info.txt"
       echo "Source: $SOURCE_DIR" >> "${BACKUP_DIR}/backup_info.txt"
       
       log_message "Backup completed successfully"
   }

   cleanup_old_backups() {
       log_message "Cleaning up backups older than $RETENTION_DAYS days"
       find "$BACKUP_BASE" -maxdepth 1 -type d -name "backup_*" -mtime +$RETENTION_DAYS -exec rm -rf {} \;
       log_message "Cleanup completed"
   }

   # Main execution
   main() {
       log_message "=== Backup Process Started ==="
       check_prerequisites
       perform_backup
       cleanup_old_backups
       log_message "=== Backup Process Completed ==="
   }

   # Error handling
   trap 'log_message "ERROR: Backup failed on line $LINENO"' ERR

   main "$@"

## RAID Management Tools

### RAID Status Checker

```python

   #!/usr/bin/env python3
   """
   RAID Status Checker for Ubuntu 22.04
   Monitors software RAID arrays and hardware RAID controllers
   """

   import subprocess
   import re
   import json
   from pathlib import Path

   class RAIDMonitor:
       def __init__(self):
           self.mdstat_path = Path('/proc/mdstat')
       
       def check_software_raid(self):
           """Check software RAID status from /proc/mdstat"""
           if not self.mdstat_path.exists():
               return {"status": "no_raid", "message": "No software RAID detected"}
           
           try:
               with open(self.mdstat_path, 'r') as f:
                   content = f.read()
               
               arrays = []
               lines = content.split('\n')
               
               for i, line in enumerate(lines):
                   if line.startswith('md'):
                       array_info = self.parse_md_line(line, lines[i+1:])
                       arrays.append(array_info)
               
               return {"status": "active", "arrays": arrays}
           
           except Exception as e:
               return {"status": "error", "message": str(e)}
       
       def parse_md_line(self, md_line, following_lines):
           """Parse mdstat line for array information"""
           parts = md_line.split()
           array_name = parts[0]
           array_status = parts[2] if len(parts) > 2 else "unknown"
           
           # Look for status in following lines
           status_line = ""
           for line in following_lines:
               if line.strip() and not line.startswith('md'):
                   status_line = line.strip()
                   break
           
           # Check for rebuild/sync status
           rebuild_match = re.search(r'\[.*\]\s+.*=\s*(\d+\.\d+)%', status_line)
           
           return {
               "name": array_name,
               "status": array_status,
               "devices": self.extract_devices(md_line),
               "rebuilding": rebuild_match.group(1) if rebuild_match else None,
               "details": status_line
           }
       
       def extract_devices(self, md_line):
           """Extract device list from md line"""
           # Simple extraction - could be enhanced
           devices = re.findall(r'[a-z]+\d+\[\d+\]', md_line)
           return [dev.split('[')[0] for dev in devices]
       
       def check_hardware_raid(self):
           """Check hardware RAID controllers"""
           controllers = []
           
           # Check for MegaRAID
           try:
               result = subprocess.run(['megacli', '-AdpAllInfo', '-aALL'], 
                                     capture_output=True, text=True)
               if result.returncode == 0:
                   controllers.append({"type": "MegaRAID", "status": "detected"})
           except FileNotFoundError:
               pass
           
           # Check for HP Smart Array
           try:
               result = subprocess.run(['hpacucli', 'ctrl', 'all', 'show'], 
                                     capture_output=True, text=True)
               if result.returncode == 0:
                   controllers.append({"type": "HP Smart Array", "status": "detected"})
           except FileNotFoundError:
               pass
           
           return controllers
       
       def get_full_status(self):
           """Get complete RAID status report"""
           report = {
               "timestamp": subprocess.run(['date'], capture_output=True, text=True).stdout.strip(),
               "software_raid": self.check_software_raid(),
               "hardware_raid": self.check_hardware_raid()
           }
           
           return report

   def main():
       monitor = RAIDMonitor()
       status = monitor.get_full_status()
       print(json.dumps(status, indent=2))

   if __name__ == "__main__":
       main()

## LVM Automation Scripts

### Dynamic LV Resize Script

```bash

   #!/bin/bash
   # Dynamic Logical Volume Resize Script
   # Automatically extends LV when usage exceeds threshold

   set -euo pipefail

   # Configuration
   THRESHOLD=85
   EXTEND_SIZE="1G"
   LOG_FILE="/var/log/lv-autoresize.log"

   log_message() {
       echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
   }

   check_lv_usage() {
       local lv_path="$1"
       local usage
       
       usage=$(df "$lv_path" | awk 'NR==2 {print $5}' | sed 's/%//')
       echo "$usage"
   }

   extend_logical_volume() {
       local lv_path="$1"
       local vg_name="$2"
       local lv_name="$3"
       
       log_message "Extending $lv_path by $EXTEND_SIZE"
       
       # Check VG free space
       local free_space
       free_space=$(vgs --noheadings -o vg_free --units g "$vg_name" | awk '{print $1}' | sed 's/g//')
       
       if (( $(echo "$free_space < 1" | bc -l) )); then
           log_message "ERROR: Not enough free space in VG $vg_name"
           return 1
       fi
       
       # Extend LV
       if lvextend -L "+$EXTEND_SIZE" "/dev/$vg_name/$lv_name"; then
           # Resize filesystem
           if resize2fs "/dev/$vg_name/$lv_name"; then
               log_message "Successfully extended $lv_path"
               return 0
           else
               log_message "ERROR: Failed to resize filesystem for $lv_path"
               return 1
           fi
       else
           log_message "ERROR: Failed to extend LV $lv_path"
           return 1
       fi
   }

   monitor_logical_volumes() {
       # Get all LVs
       while IFS= read -r line; do
           local lv_path vg_name lv_name
           lv_path=$(echo "$line" | awk '{print $1}')
           vg_name=$(echo "$line" | awk '{print $2}')
           lv_name=$(echo "$line" | awk '{print $3}')
           
           if [[ -n "$lv_path" && "$lv_path" != "LV" ]]; then
               local usage
               usage=$(check_lv_usage "$lv_path")
               
               if [[ "$usage" -gt "$THRESHOLD" ]]; then
                   log_message "WARNING: $lv_path usage is ${usage}%, threshold is ${THRESHOLD}%"
                   extend_logical_volume "$lv_path" "$vg_name" "$lv_name"
               else
                   log_message "INFO: $lv_path usage is ${usage}% (OK)"
               fi
           fi
       done < <(lvs --noheadings -o lv_path,vg_name,lv_name)
   }

   main() {
       if [[ $EUID -ne 0 ]]; then
           echo "This script must be run as root"
           exit 1
       fi
       
       log_message "=== LV Auto-resize Monitor Started ==="
       monitor_logical_volumes
       log_message "=== LV Auto-resize Monitor Completed ==="
   }

   main "$@"

## Network Storage Utilities

NFS Mount Manager
~~~~~~~~~~~~~~~~

```python

   #!/usr/bin/env python3
   """
   NFS Mount Manager for Ubuntu 22.04
   Manages NFS mounts with health checking and auto-recovery
   """

   import subprocess
   import yaml
   import os
   import sys
   from pathlib import Path

   class NFSManager:
       def __init__(self, config_file='/etc/nfs-mounts.yaml'):
           self.config_file = config_file
           self.config = self.load_config()
       
       def load_config(self):
           """Load NFS mount configuration"""
           default_config = {
               'mounts': [
                   {
                       'server': '192.168.1.100',
                       'export': '/export/shared',
                       'mountpoint': '/mnt/nfs-shared',
                       'options': 'rw,sync,hard,intr',
                       'auto_mount': True
                   }
               ],
               'timeout': 30,
               'retry_count': 3
           }
           
           if Path(self.config_file).exists():
               try:
                   with open(self.config_file, 'r') as f:
                       return yaml.safe_load(f)
               except Exception as e:
                   print(f"Error loading config: {e}")
                   return default_config
           else:
               self.save_config(default_config)
               return default_config
       
       def save_config(self, config):
           """Save configuration to file"""
           try:
               with open(self.config_file, 'w') as f:
                   yaml.dump(config, f, default_flow_style=False)
           except Exception as e:
               print(f"Error saving config: {e}")
       
       def check_nfs_server(self, server):
           """Check if NFS server is reachable"""
           try:
               result = subprocess.run(['ping', '-c', '1', '-W', '5', server],
                                     capture_output=True, text=True)
               return result.returncode == 0
           except Exception:
               return False
       
       def is_mounted(self, mountpoint):
           """Check if mountpoint is currently mounted"""
           try:
               result = subprocess.run(['mountpoint', '-q', mountpoint])
               return result.returncode == 0
           except Exception:
               return False
       
       def mount_nfs(self, mount_config):
           """Mount an NFS share"""
           server = mount_config['server']
           export = mount_config['export']
           mountpoint = mount_config['mountpoint']
           options = mount_config.get('options', 'rw,sync')
           
           print(f"Mounting {server}:{export} -> {mountpoint}")
           
           # Create mountpoint if it doesn't exist
           Path(mountpoint).mkdir(parents=True, exist_ok=True)
           
           # Check if already mounted
           if self.is_mounted(mountpoint):
               print(f"  Already mounted: {mountpoint}")
               return True
           
           # Check server connectivity
           if not self.check_nfs_server(server):
               print(f"  ERROR: Cannot reach NFS server {server}")
               return False
           
           # Mount the share
           try:
               nfs_source = f"{server}:{export}"
               cmd = ['mount', '-t', 'nfs', '-o', options, nfs_source, mountpoint]
               result = subprocess.run(cmd, capture_output=True, text=True)
               
               if result.returncode == 0:
                   print(f"  Successfully mounted {mountpoint}")
                   return True
               else:
                   print(f"  ERROR: Mount failed: {result.stderr}")
                   return False
           
           except Exception as e:
               print(f"  ERROR: Exception during mount: {e}")
               return False
       
       def unmount_nfs(self, mountpoint):
           """Unmount an NFS share"""
           try:
               if self.is_mounted(mountpoint):
                   result = subprocess.run(['umount', mountpoint],
                                         capture_output=True, text=True)
                   if result.returncode == 0:
                       print(f"Successfully unmounted {mountpoint}")
                       return True
                   else:
                       print(f"ERROR: Unmount failed: {result.stderr}")
                       return False
               else:
                   print(f"{mountpoint} is not mounted")
                   return True
           except Exception as e:
               print(f"ERROR: Exception during unmount: {e}")
               return False
       
       def mount_all(self):
           """Mount all configured NFS shares"""
           success_count = 0
           total_count = len(self.config['mounts'])
           
           for mount_config in self.config['mounts']:
               if mount_config.get('auto_mount', True):
                   if self.mount_nfs(mount_config):
                       success_count += 1
           
           print(f"Mounted {success_count}/{total_count} NFS shares")
           return success_count == total_count
       
       def unmount_all(self):
           """Unmount all configured NFS shares"""
           for mount_config in self.config['mounts']:
               self.unmount_nfs(mount_config['mountpoint'])
       
       def health_check(self):
           """Check health of all NFS mounts"""
           print("NFS Mount Health Check")
           print("=" * 50)
           
           for mount_config in self.config['mounts']:
               server = mount_config['server']
               mountpoint = mount_config['mountpoint']
               
               print(f"Checking {server}:{mount_config['export']}")
               
               # Check server
               server_ok = self.check_nfs_server(server)
               print(f"  Server reachable: {'YES' if server_ok else 'NO'}")
               
               # Check mount
               mounted = self.is_mounted(mountpoint)
               print(f"  Mounted: {'YES' if mounted else 'NO'}")
               
               # Check accessibility
               if mounted:
                   try:
                       test_file = Path(mountpoint) / '.nfs_test'
                       test_file.touch()
                       test_file.unlink()
                       print("  Accessible: YES")
                   except Exception:
                       print("  Accessible: NO")
               
               print()

   def main():
       if len(sys.argv) < 2:
           print("Usage: nfs-manager.py {mount|unmount|health|mount-all|unmount-all}")
           sys.exit(1)
       
       if os.geteuid() != 0:
           print("This script must be run as root")
           sys.exit(1)
       
       manager = NFSManager()
       command = sys.argv[1]
       
       if command == "mount-all":
           manager.mount_all()
       elif command == "unmount-all":
           manager.unmount_all()
       elif command == "health":
           manager.health_check()
       else:
           print(f"Unknown command: {command}")

   if __name__ == "__main__":
       main()

## File System Utilities

### Filesystem Health Checker

```bash

   #!/bin/bash
   # Comprehensive Filesystem Health Checker for Ubuntu 22.04

   set -euo pipefail

   # Configuration
   LOG_FILE="/var/log/filesystem-health.log"
   REPORT_FILE="/tmp/filesystem-health-report.txt"

   log_message() {
       echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
   }

   check_filesystem_errors() {
       local device="$1"
       local fstype="$2"
       local mountpoint="$3"
       
       log_message "Checking filesystem errors for $device ($fstype)"
       
       case "$fstype" in
           ext4|ext3|ext2)
               # Check for ext filesystem errors
               local error_count
               error_count=$(tune2fs -l "$device" 2>/dev/null | grep "Filesystem errors behavior" || echo "0")
               
               if dumpe2fs -h "$device" 2>/dev/null | grep -q "has_journal"; then
                   log_message "  Journal filesystem detected"
               fi
               
               # Force check if needed
               local mount_count max_count
               mount_count=$(tune2fs -l "$device" 2>/dev/null | grep "Mount count:" | awk '{print $3}' || echo "0")
               max_count=$(tune2fs -l "$device" 2>/dev/null | grep "Maximum mount count:" | awk '{print $4}' || echo "0")
               
               if [[ "$max_count" -gt 0 && "$mount_count" -gt "$max_count" ]]; then
                   log_message "  WARNING: Mount count ($mount_count) exceeds maximum ($max_count)"
               fi
               ;;
           
           xfs)
               # Check XFS filesystem
               if xfs_info "$mountpoint" >/dev/null 2>&1; then
                   log_message "  XFS filesystem appears healthy"
               else
                   log_message "  WARNING: XFS filesystem check failed"
               fi
               ;;
           
           btrfs)
               # Check Btrfs filesystem
               if btrfs filesystem show "$device" >/dev/null 2>&1; then
                   local errors
                   errors=$(btrfs device stats "$device" 2>/dev/null | grep -c "err" || echo "0")
                   log_message "  Btrfs error count: $errors"
               fi
               ;;
       esac
   }

   check_disk_usage() {
       log_message "Checking disk usage patterns"
       
       df -h | while IFS= read -r line; do
           if [[ "$line" == *"% /"* ]]; then
               local usage
               usage=$(echo "$line" | awk '{print $5}' | sed 's/%//')
               local mountpoint
               mountpoint=$(echo "$line" | awk '{print $6}')
               
               if [[ "$usage" -gt 90 ]]; then
                   log_message "  CRITICAL: $mountpoint is ${usage}% full"
               elif [[ "$usage" -gt 80 ]]; then
                   log_message "  WARNING: $mountpoint is ${usage}% full"
               fi
           fi
       done
   }

   check_inode_usage() {
       log_message "Checking inode usage"
       
       df -i | while IFS= read -r line; do
           if [[ "$line" == *"% /"* ]]; then
               local usage
               usage=$(echo "$line" | awk '{print $5}' | sed 's/%//')
               local mountpoint
               mountpoint=$(echo "$line" | awk '{print $6}')
               
               if [[ "$usage" -gt 90 ]]; then
                   log_message "  CRITICAL: $mountpoint inodes ${usage}% used"
               elif [[ "$usage" -gt 80 ]]; then
                   log_message "  WARNING: $mountpoint inodes ${usage}% used"
               fi
           fi
       done
   }

   generate_report() {
       {
           echo "Filesystem Health Report"
           echo "Generated: $(date)"
           echo "=========================================="
           echo
           
           echo "DISK USAGE:"
           df -h
           echo
           
           echo "INODE USAGE:"
           df -i
           echo
           
           echo "MOUNTED FILESYSTEMS:"
           mount | grep -E '^/dev/'
           echo
           
           echo "FILESYSTEM TYPES:"
           lsblk -f
           echo
           
           echo "RECENT LOG ENTRIES:"
           tail -20 "$LOG_FILE"
           
       } > "$REPORT_FILE"
       
       log_message "Health report generated: $REPORT_FILE"
   }

   main() {
       if [[ $EUID -ne 0 ]]; then
           echo "This script should be run as root for complete checks"
       fi
       
       log_message "=== Filesystem Health Check Started ==="
       
       # Get mounted filesystems
       while IFS= read -r line; do
           if [[ "$line" == /dev/* ]]; then
               local device fstype mountpoint
               device=$(echo "$line" | awk '{print $1}')
               fstype=$(echo "$line" | awk '{print $3}')
               mountpoint=$(echo "$line" | awk '{print $2}')
               
               check_filesystem_errors "$device" "$fstype" "$mountpoint"
           fi
       done < <(mount | grep -E '^/dev/')
       
       check_disk_usage
       check_inode_usage
       generate_report
       
       log_message "=== Filesystem Health Check Completed ==="
       
       echo "Health check completed. Report available at: $REPORT_FILE"
       echo "Log file: $LOG_FILE"
   }

   main "$@"

Performance Testing Scripts
--------------------------

### Storage Benchmark Suite

```python

   #!/usr/bin/env python3
   """
   Storage Performance Benchmark Suite for Ubuntu 22.04
   Tests various storage scenarios and generates performance reports
   """

   import subprocess
   import time
   import json
   import os
   import sys
   from pathlib import Path

   class StorageBenchmark:
       def __init__(self, test_dir="/tmp/storage_test"):
           self.test_dir = Path(test_dir)
           self.test_dir.mkdir(exist_ok=True)
           self.results = {}
       
       def run_dd_test(self, test_name, block_size="1M", count=1024):
           """Run DD-based I/O test"""
           test_file = self.test_dir / f"{test_name}.dat"
           
           # Write test
           write_start = time.time()
           cmd = ['dd', f'if=/dev/zero', f'of={test_file}', 
                  f'bs={block_size}', f'count={count}', 'conv=fdatasync']
           
           try:
               result = subprocess.run(cmd, capture_output=True, text=True)
               write_time = time.time() - write_start
               
               # Parse DD output for speed
               write_speed = self.parse_dd_output(result.stderr)
               
               # Read test
               read_start = time.time()
               cmd = ['dd', f'if={test_file}', 'of=/dev/null', f'bs={block_size}']
               result = subprocess.run(cmd, capture_output=True, text=True)
               read_time = time.time() - read_start
               
               read_speed = self.parse_dd_output(result.stderr)
               
               # Cleanup
               test_file.unlink()
               
               return {
                   'write_time': write_time,
                   'read_time': read_time,
                   'write_speed': write_speed,
                   'read_speed': read_speed,
                   'block_size': block_size,
                   'data_size': f"{count}{block_size}"
               }
           
           except Exception as e:
               return {'error': str(e)}
       
       def parse_dd_output(self, dd_stderr):
           """Parse DD output to extract transfer rate"""
           import re
           
           # Look for patterns like "1.0 GB/s" or "500 MB/s"
           pattern = r'(\d+\.?\d*)\s*([KMGT]?B/s)'
           match = re.search(pattern, dd_stderr)
           
           if match:
               return f"{match.group(1)} {match.group(2)}"
           return "Unknown"
       
       def run_fio_test(self, test_name, job_config):
           """Run FIO benchmark if available"""
           try:
               # Check if fio is available
               subprocess.run(['which', 'fio'], check=True, capture_output=True)
               
               # Create FIO job file
               job_file = self.test_dir / f"{test_name}.fio"
               with open(job_file, 'w') as f:
                   f.write(job_config)
               
               # Run FIO
               result = subprocess.run(['fio', str(job_file), '--output-format=json'],
                                     capture_output=True, text=True)
               
               if result.returncode == 0:
                   fio_data = json.loads(result.stdout)
                   job_file.unlink()
                   return fio_data
               else:
                   return {'error': result.stderr}
           
           except (subprocess.CalledProcessError, FileNotFoundError):
               return {'error': 'FIO not available'}
       
       def run_sequential_tests(self):
           """Run sequential I/O tests"""
           print("Running sequential I/O tests...")
           
           # Various block sizes
           block_sizes = ['4K', '64K', '1M', '4M']
           
           for bs in block_sizes:
               test_name = f"sequential_{bs}"
               print(f"  Testing {bs} blocks...")
               result = self.run_dd_test(test_name, bs, 256 if bs == '4M' else 1024)
               self.results[test_name] = result
       
       def run_random_tests(self):
           """Run random I/O tests using FIO"""
           print("Running random I/O tests...")
           
           # Random read test
           random_read_config = """
   [random_read]
   ioengine=libaio
   rw=randread
   bs=4k
   direct=1
   size=100M
   numjobs=1
   runtime=30
   group_reporting
   filename={}/random_read.dat
   """.format(self.test_dir)
           
           result = self.run_fio_test("random_read", random_read_config)
           self.results['random_read'] = result
           
           # Random write test
           random_write_config = """
   [random_write]
   ioengine=libaio
   rw=randwrite
   bs=4k
   direct=1
   size=100M
   numjobs=1
   runtime=30
   group_reporting
   filename={}/random_write.dat
   """.format(self.test_dir)
           
           result = self.run_fio_test("random_write", random_write_config)
           self.results['random_write'] = result
       
       def generate_report(self):
           """Generate performance report"""
           report_file = self.test_dir / "benchmark_report.json"
           
           report = {
               'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
               'test_directory': str(self.test_dir),
               'system_info': self.get_system_info(),
               'results': self.results
           }
           
           with open(report_file, 'w') as f:
               json.dump(report, f, indent=2)
           
           # Generate human-readable summary
           self.print_summary()
           
           print(f"\nDetailed report saved to: {report_file}")
       
       def get_system_info(self):
           """Get system information"""
           try:
               # Get CPU info
               cpu_info = subprocess.run(['lscpu'], capture_output=True, text=True).stdout
               
               # Get memory info
               mem_info = subprocess.run(['free', '-h'], capture_output=True, text=True).stdout
               
               # Get storage info
               storage_info = subprocess.run(['lsblk'], capture_output=True, text=True).stdout
               
               return {
                   'cpu': cpu_info.split('\n')[:10],  # First 10 lines
                   'memory': mem_info,
                   'storage': storage_info
               }
           except Exception:
               return {'error': 'Could not gather system info'}
       
       def print_summary(self):
           """Print benchmark summary"""
           print("\n" + "="*60)
           print("STORAGE BENCHMARK SUMMARY")
           print("="*60)
           
           for test_name, result in self.results.items():
               if 'error' not in result:
                   print(f"\n{test_name.upper()}:")
                   if 'write_speed' in result:
                       print(f"  Write Speed: {result['write_speed']}")
                       print(f"  Read Speed:  {result['read_speed']}")
                   elif 'jobs' in result:  # FIO result
                       for job in result['jobs']:
                           if 'read' in job:
                               iops = job['read'].get('iops', 'N/A')
                               bw = job['read'].get('bw', 'N/A')
                               print(f"  Read IOPS:   {iops}")
                               print(f"  Read BW:     {bw} KB/s")
                           if 'write' in job:
                               iops = job['write'].get('iops', 'N/A')
                               bw = job['write'].get('bw', 'N/A')
                               print(f"  Write IOPS:  {iops}")
                               print(f"  Write BW:    {bw} KB/s")
               else:
                   print(f"\n{test_name.upper()}: ERROR - {result['error']}")
       
       def run_all_tests(self):
           """Run complete benchmark suite"""
           print("Starting Storage Benchmark Suite")
           print("This may take several minutes...")
           
           self.run_sequential_tests()
           self.run_random_tests()
           self.generate_report()
           
           # Cleanup
           for file in self.test_dir.glob("*.dat"):
               file.unlink()

   def main():
       if len(sys.argv) > 1:
           test_dir = sys.argv[1]
       else:
           test_dir = "/tmp/storage_test"
       
       benchmark = StorageBenchmark(test_dir)
       benchmark.run_all_tests()

   if __name__ == "__main__":
       main()

## Installation and Usage Instructions

### Setting Up the Environment

```bash

   # Install required packages
   sudo apt update
   sudo apt install -y python3-pip smartmontools fio

   # Install Python dependencies
   pip3 install pyyaml

   # Make scripts executable
   chmod +x *.py *.sh

   # Create necessary directories
   sudo mkdir -p /var/log /backup

Script Configuration
~~~~~~~~~~~~~~~~~~~

**Storage Monitor Configuration:**

```bash

   # Set up cron job for automated monitoring
   echo "0 */6 * * * root /path/to/storage-monitor.py" | sudo tee -a /etc/crontab

   # Configure log rotation
   sudo tee /etc/logrotate.d/storage-monitor << EOF
   /var/log/storage-monitor.log {
       daily
       rotate 30
       compress
       missingok
       create 644 root root
   }
   EOF

**NFS Manager Setup:**

```bash

   # Install NFS utilities
   sudo apt install -y nfs-common

   # Create configuration file
   sudo tee /etc/nfs-mounts.yaml << EOF
   mounts:
     - server: "your-nfs-server.local"
       export: "/export/data"
       mountpoint: "/mnt/nfs-data"
       options: "rw,sync,hard,intr"
       auto_mount: true
   timeout: 30
   retry_count: 3
   EOF

Integration Examples
-------------------

Systemd Service Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~

```ini

   # /etc/systemd/system/storage-monitor.service
   [Unit]
   Description=Storage Health Monitor
   After=multi-user.target

   [Service]
   Type=oneshot
   ExecStart=/usr/local/bin/storage-monitor.py
   User=root

   [Install]
   WantedBy=multi-user.target

```bash

   # Enable and start the service
   sudo systemctl daemon-reload
   sudo systemctl enable storage-monitor.service
   sudo systemctl start storage-monitor.service

### Custom Alerts Integration

```python

   # Email alert integration
   import smtplib
   from email.mime.text import MIMEText

   def send_alert(subject, message):
       msg = MIMEText(message)
       msg['Subject'] = subject
       msg['From'] = 'storage-monitor@yourserver.com'
       msg['To'] = 'admin@yourserver.com'
       
       server = smtplib.SMTP('localhost')
       server.send_message(msg)
       server.quit()

These scripts provide a comprehensive foundation for storage management automation on Ubuntu 22.04. They can be customized and extended based on specific requirements and integrated into larger system management frameworks.

```

---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---