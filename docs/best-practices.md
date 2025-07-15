# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

# Best Practices and Guidelines

This section outlines industry best practices and proven guidelines for storage management on Ubuntu 22.04.

   :local:
   :depth: 2

## Storage Planning and Design

Capacity Planning
~~~~~~~~~~~~~~~~

**Growth Assessment:**

- Plan for 3-5 years of growth
- Account for data growth rates: 20-40% annually for typical business environments
- Include overhead for snapshots, backups, and temporary files
- Reserve 10-15% free space for optimal performance

**Performance Requirements:**

```bash

   # Benchmark current workload
   iotop -a -o -d 1 | head -20
   
   # Monitor I/O patterns
   iostat -x 1 60 | tee io-analysis.log
   
   # Calculate IOPS requirements
   # Sequential workloads: 100-500 IOPS
   # Random workloads: 1000-10000+ IOPS
   # Database workloads: 5000-50000+ IOPS

**Storage Hierarchy Design:**

1. **Hot Data** (frequently accessed)
   - NVMe SSD for highest performance
   - Direct attachment or high-speed SAN

2. **Warm Data** (regularly accessed)
   - SATA SSD or high-performance HDD
   - Network storage with good connectivity

3. **Cold Data** (archival/backup)
   - High-capacity HDD
   - Object storage or tape for long-term retention

Filesystem Selection Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ext4 - General Purpose:**

```bash

   # Optimal for most workloads
   sudo mkfs.ext4 -E stride=32,stripe-width=64 /dev/sdX1
   
   # Mount options for performance
   mount -o noatime,nodiratime,data=writeback /dev/sdX1 /mnt

*Use Cases:* Boot partitions, general file storage, databases with simple requirements

**XFS - High Performance:**

```bash

   # Create with optimal settings
   sudo mkfs.xfs -f -s size=4096 -d agcount=8 /dev/sdX1
   
   # Mount with performance options
   mount -o noatime,logbsize=256k,largeio /dev/sdX1 /mnt

*Use Cases:* Large files, high-throughput applications, media streaming

**Btrfs - Advanced Features:**

```bash

   # Create with metadata redundancy
   sudo mkfs.btrfs -m raid1 -d single /dev/sdX1 /dev/sdX2
   
   # Enable compression
   mount -o compress=zstd,noatime /dev/sdX1 /mnt

*Use Cases:* Development environments, systems requiring snapshots, data integrity critical applications

**ZFS - Enterprise Features:**

```bash

   # Install ZFS
   sudo apt install zfsutils-linux
   
   # Create pool with redundancy
   sudo zpool create -o ashift=12 tank raidz2 /dev/sd[abcd]1
   
   # Create filesystem with compression
   sudo zfs create -o compression=lz4 tank/data

*Use Cases:* Enterprise storage, virtualization, backup systems

## Partitioning Best Practices

Partition Layout Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

**Standard Desktop/Server Layout:**

```bash

   # Create GPT partition table
   sudo parted /dev/sdX mklabel gpt
   
   # UEFI boot partition (512MB)
   sudo parted /dev/sdX mkpart primary fat32 1MiB 513MiB
   sudo parted /dev/sdX set 1 esp on
   
   # Root partition (20-50GB minimum)
   sudo parted /dev/sdX mkpart primary ext4 513MiB 50GiB
   
   # Home partition (remaining space)
   sudo parted /dev/sdX mkpart primary ext4 50GiB 100%

**Server Layout with Separate Partitions:**

```bash

   # Boot partition (1GB)
   sudo parted /dev/sdX mkpart primary ext4 1MiB 1GiB
   
   # Root partition (20GB)
   sudo parted /dev/sdX mkpart primary ext4 1GiB 21GiB
   
   # Var partition (10GB minimum)
   sudo parted /dev/sdX mkpart primary ext4 21GiB 31GiB
   
   # Home partition (as needed)
   sudo parted /dev/sdX mkpart primary ext4 31GiB 131GiB
   
   # Tmp partition (5GB)
   sudo parted /dev/sdX mkpart primary ext4 131GiB 136GiB

**LVM-based Layout:**

```bash

   # Create LVM partition
   sudo parted /dev/sdX mkpart primary 513MiB 100%
   sudo parted /dev/sdX set 2 lvm on
   
   # Initialize LVM
   sudo pvcreate /dev/sdX2
   sudo vgcreate vg0 /dev/sdX2
   
   # Create logical volumes
   sudo lvcreate -L 20G -n root vg0
   sudo lvcreate -L 10G -n var vg0
   sudo lvcreate -L 50G -n home vg0
   sudo lvcreate -L 4G -n swap vg0

Alignment and Performance
~~~~~~~~~~~~~~~~~~~~~~~~

**Sector Alignment:**

```bash

   # Check disk sector size
   sudo fdisk -l /dev/sdX | grep "Sector size"
   
   # For 4K sectors, align to 4096-byte boundaries
   sudo parted /dev/sdX mkpart primary 4096s 100%
   
   # For SSDs, align to 1MiB boundaries
   sudo parted /dev/sdX mkpart primary 1MiB 100%

## Security Best Practices

Encryption at Rest
~~~~~~~~~~~~~~~~~

**LUKS Full Disk Encryption:**

```bash

   # Encrypt partition
   sudo cryptsetup luksFormat /dev/sdX1
   
   # Open encrypted device
   sudo cryptsetup luksOpen /dev/sdX1 encrypted_root
   
   # Format encrypted device
   sudo mkfs.ext4 /dev/mapper/encrypted_root
   
   # Add to crypttab
   echo "encrypted_root /dev/sdX1 none luks" | sudo tee -a /etc/crypttab

**Directory-level Encryption:**

```bash

   # Install eCryptfs
   sudo apt install ecryptfs-utils
   
   # Encrypt home directory
   sudo ecryptfs-migrate-home -u username
   
   # Or encrypt specific directories
   sudo mount -t ecryptfs /secure /secure

### Access Control and Permissions

**Principle of Least Privilege:**

```bash

   # Set restrictive default permissions
   umask 027
   
   # Use groups for shared access
   sudo groupadd storage-users
   sudo usermod -a -G storage-users username
   
   # Set group ownership and permissions
   sudo chgrp -R storage-users /shared/storage
   sudo chmod -R 750 /shared/storage

**File System Extended Attributes:**

```bash

   # Enable ACLs on filesystem
   sudo mount -o remount,acl /dev/sdX1
   
   # Set Access Control Lists
   setfacl -m u:username:rw /secure/file.txt
   setfacl -m g:groupname:r /secure/directory
   
   # View ACLs
   getfacl /secure/file.txt

**Immutable Files:**

```bash

   # Make file immutable
   sudo chattr +i /critical/config.file
   
   # Make file append-only
   sudo chattr +a /var/log/audit.log
   
   # View attributes
   lsattr /critical/config.file

## Backup and Recovery Strategies

Backup Strategy Framework
~~~~~~~~~~~~~~~~~~~~~~~~

**3-2-1 Rule Implementation:**

- **3** copies of important data
- **2** different storage media types
- **1** copy stored off-site

**Backup Types and Schedule:**

```bash

   # Full backup (weekly)
   tar -czf /backup/full-$(date +%Y%m%d).tar.gz /home /etc /var/log
   
   # Incremental backup (daily)
   rsync -av --link-dest=/backup/last-backup /home/ /backup/incremental-$(date +%Y%m%d)/
   
   # Differential backup (daily)
   tar -czf /backup/diff-$(date +%Y%m%d).tar.gz --newer-mtime="1 day ago" /home

**Automated Backup Script:**

```bash

   #!/bin/bash
   # /usr/local/bin/backup-manager.sh
   
   BACKUP_ROOT="/backup"
   SOURCE_DIRS="/home /etc /var/log"
   RETENTION_DAYS=30
   LOG_FILE="/var/log/backup.log"
   
   log_message() {
       echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
   }
   
   perform_backup() {
       local backup_type="$1"
       local backup_dir="$BACKUP_ROOT/$backup_type-$(date +%Y%m%d_%H%M%S)"
       
       mkdir -p "$backup_dir"
       
       case "$backup_type" in
           "full")
               tar -czf "$backup_dir/system.tar.gz" $SOURCE_DIRS
               ;;
           "incremental")
               local last_backup=$(find "$BACKUP_ROOT" -name "incremental-*" | sort | tail -1)
               rsync -av --link-dest="$last_backup" $SOURCE_DIRS "$backup_dir/"
               ;;
       esac
       
       # Create checksum
       find "$backup_dir" -type f -exec sha256sum {} \; > "$backup_dir/checksums.sha256"
       
       log_message "Backup completed: $backup_dir"
   }
   
   cleanup_old_backups() {
       find "$BACKUP_ROOT" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
       log_message "Cleaned up backups older than $RETENTION_DAYS days"
   }
   
   # Run backup based on day of week
   if [ "$(date +%u)" -eq 7 ]; then
       perform_backup "full"
   else
       perform_backup "incremental"
   fi
   
   cleanup_old_backups

**Backup Verification:**

```bash

   # Verify backup integrity
   #!/bin/bash
   verify_backup() {
       local backup_dir="$1"
       
       # Check checksums
       cd "$backup_dir"
       sha256sum -c checksums.sha256
       
       # Test archive extraction
       if [ -f system.tar.gz ]; then
           tar -tzf system.tar.gz > /dev/null && echo "Archive OK" || echo "Archive CORRUPTED"
       fi
       
       # Check file count
       local file_count=$(find . -type f | wc -l)
       echo "Files in backup: $file_count"
   }

Recovery Planning
~~~~~~~~~~~~~~~~

**Recovery Time Objective (RTO) and Recovery Point Objective (RPO):**

- **Critical Systems:** RTO < 4 hours, RPO < 1 hour
- **Important Systems:** RTO < 24 hours, RPO < 4 hours
- **Standard Systems:** RTO < 72 hours, RPO < 24 hours

**Disaster Recovery Procedures:**

```bash

   # Create disaster recovery documentation
   cat > /etc/disaster-recovery.md << 'EOF'
   # Disaster Recovery Procedures
   
   ## Critical Information
   - Backup Location: /backup and remote://backup-server/
   - Recovery Media: Ubuntu 22.04 Live USB
   - Key Personnel: admin@company.com, +1-555-0123
   
   ## Recovery Steps
   1. Boot from recovery media
   2. Identify storage devices: `lsblk`
   3. Mount backup location
   4. Restore from most recent backup
   5. Verify system integrity
   6. Update disaster recovery log
   EOF

Performance Optimization
-----------------------

I/O Optimization
~~~~~~~~~~~~~~~

**I/O Scheduler Tuning:**

```bash

   # Check current scheduler
   cat /sys/block/sdX/queue/scheduler
   
   # Set optimal scheduler per device type
   # For SSDs
   echo none | sudo tee /sys/block/nvme0n1/queue/scheduler
   
   # For HDDs
   echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
   
   # Make permanent
   echo 'ACTION=="add|change", KERNEL=="sd[a-z]*", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="none"' | sudo tee /etc/udev/rules.d/60-ssd-scheduler.rules

**Read-ahead Optimization:**

```bash

   # Check current read-ahead
   sudo blockdev --getra /dev/sdX
   
   # Set read-ahead for sequential workloads
   sudo blockdev --setra 4096 /dev/sdX  # For large files
   sudo blockdev --setra 256 /dev/sdX   # For random access

**Mount Options for Performance:**

```bash

   # High-performance mount options
   # /etc/fstab entries:
   
   # For databases (ext4)
   /dev/mapper/db-data /var/lib/mysql ext4 noatime,nodiratime,data=writeback,barrier=0 0 2
   
   # For web servers (ext4)
   /dev/mapper/web-data /var/www ext4 noatime,nodiratime,data=ordered 0 2
   
   # For temporary files
   tmpfs /tmp tmpfs defaults,noatime,size=2G 0 0

Memory and Cache Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**File System Cache Tuning:**

```bash

   # Adjust dirty page writeback
   echo 5 | sudo tee /proc/sys/vm/dirty_ratio
   echo 2 | sudo tee /proc/sys/vm/dirty_background_ratio
   
   # Reduce swappiness for database servers
   echo 1 | sudo tee /proc/sys/vm/swappiness
   
   # Make changes permanent
   echo "vm.dirty_ratio = 5" | sudo tee -a /etc/sysctl.conf
   echo "vm.dirty_background_ratio = 2" | sudo tee -a /etc/sysctl.conf
   echo "vm.swappiness = 1" | sudo tee -a /etc/sysctl.conf

## Monitoring and Alerting

Proactive Monitoring
~~~~~~~~~~~~~~~~~~~

**Key Metrics to Monitor:**

1. **Storage Capacity:** Disk usage, inode usage, growth trends
2. **Performance:** IOPS, throughput, latency, queue depth
3. **Health:** SMART status, error rates, temperature
4. **Availability:** Mount status, filesystem errors, RAID status

**Monitoring Script:**

```bash

   #!/bin/bash
   # /usr/local/bin/storage-monitor.sh
   
   ALERT_EMAIL="admin@company.com"
   LOG_FILE="/var/log/storage-monitor.log"
   
   # Thresholds
   DISK_USAGE_WARN=80
   DISK_USAGE_CRIT=90
   INODE_USAGE_WARN=80
   LOAD_WARN=2.0
   
   send_alert() {
       local subject="$1"
       local message="$2"
       echo "$message" | mail -s "$subject" "$ALERT_EMAIL"
       echo "$(date): ALERT - $subject - $message" >> "$LOG_FILE"
   }
   
   check_disk_usage() {
       df -h | while read filesystem size used avail percent mountpoint; do
           if [[ "$percent" =~ ([0-9]+)% ]]; then
               usage=${BASH_REMATCH[1]}
               if [ "$usage" -gt $DISK_USAGE_CRIT ]; then
                   send_alert "CRITICAL: Disk Usage" "$mountpoint is ${usage}% full"
               elif [ "$usage" -gt $DISK_USAGE_WARN ]; then
                   send_alert "WARNING: Disk Usage" "$mountpoint is ${usage}% full"
               fi
           fi
       done
   }
   
   check_smart_status() {
       for device in /dev/sd[a-z] /dev/nvme[0-9]n[0-9]; do
           if [ -b "$device" ]; then
               if ! smartctl -H "$device" | grep -q "PASSED"; then
                   send_alert "CRITICAL: SMART Failure" "Device $device failed SMART test"
               fi
           fi
       done
   }
   
   check_raid_status() {
       if [ -f /proc/mdstat ]; then
           if grep -q "_" /proc/mdstat; then
               send_alert "WARNING: RAID Degraded" "Software RAID array is degraded"
           fi
       fi
   }
   
   # Run checks
   check_disk_usage
   check_smart_status
   check_raid_status

**Automated Health Reports:**

```bash

   #!/bin/bash
   # Daily storage health report
   
   REPORT_FILE="/tmp/daily-storage-report.txt"
   
   {
       echo "Daily Storage Health Report - $(date)"
       echo "==========================================="
       echo
       
       echo "DISK USAGE:"
       df -h
       echo
       
       echo "INODE USAGE:"
       df -i
       echo
       
       echo "SYSTEM LOAD:"
       uptime
       echo
       
       echo "I/O STATISTICS (last hour):"
       sar -d -s $(date -d '1 hour ago' '+%H:%M:%S') | tail -20
       echo
       
       echo "RAID STATUS:"
       cat /proc/mdstat 2>/dev/null || echo "No software RAID detected"
       echo
       
       echo "SMART STATUS:"
       for device in /dev/sd[a-z]; do
           if [ -b "$device" ]; then
               echo "$device: $(smartctl -H "$device" | grep overall)"
           fi
       done
       
   } > "$REPORT_FILE"
   
   # Email report
   mail -s "Daily Storage Report - $(hostname)" admin@company.com < "$REPORT_FILE"

Maintenance Procedures
---------------------

Regular Maintenance Tasks
~~~~~~~~~~~~~~~~~~~~~~~~

**Weekly Tasks:**

```bash

   #!/bin/bash
   # Weekly maintenance script
   
   # SMART tests
   for device in /dev/sd[a-z]; do
       if [ -b "$device" ]; then
           smartctl -t long "$device"
       fi
   done
   
   # Filesystem checks
   find /var/log -name "*.log" -size +100M -exec logrotate -f {} \;
   
   # Clean temporary files
   find /tmp -type f -atime +7 -delete
   find /var/tmp -type f -atime +30 -delete
   
   # Update package cache
   apt update
   apt list --upgradable

**Monthly Tasks:**

```bash

   #!/bin/bash
   # Monthly maintenance script
   
   # Full system backup verification
   /usr/local/bin/verify-backups.sh
   
   # Storage capacity planning
   /usr/local/bin/capacity-report.sh
   
   # Security updates
   apt upgrade -y
   
   # Performance baseline
   /usr/local/bin/performance-benchmark.sh

Documentation and Change Management
----------------------------------

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~

**Storage Configuration Documentation:**

```bash

   # Create storage inventory
   cat > /etc/storage-inventory.yaml << 'EOF'
   storage_systems:
     - name: "Primary Storage"
       type: "LVM on RAID1"
       devices: ["/dev/sda", "/dev/sdb"]
       capacity: "2TB"
       filesystem: "ext4"
       mount_points:
         - "/": "50GB"
         - "/home": "1.5TB"
         - "/var": "200GB"
       backup_schedule: "Daily incremental, Weekly full"
       
     - name: "Database Storage"
       type: "Direct attach NVMe"
       devices: ["/dev/nvme0n1"]
       capacity: "1TB"
       filesystem: "xfs"
       mount_points:
         - "/var/lib/mysql": "800GB"
       backup_schedule: "Hourly snapshots, Daily backup"
   
   network_storage:
     - name: "Archive NFS"
       server: "nas.company.local"
       export: "/export/archive"
       mount_point: "/mnt/archive"
       options: "rw,soft,intr"
   EOF

**Change Management Process:**

1. **Document all changes** in `/var/log/storage-changes.log`
2. **Test changes** in development environment first
3. **Create rollback plan** before implementing
4. **Monitor system** after changes for 24-48 hours

These best practices provide a solid foundation for reliable, secure, and high-performing storage systems on Ubuntu 22.04. Regular review and updates of these practices ensure continued effectiveness as technology and requirements evolve.

```

---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---