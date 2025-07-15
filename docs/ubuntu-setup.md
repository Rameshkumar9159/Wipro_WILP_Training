# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

Ubuntu 22.04 Setup and Configuration
===================================

## Ubuntu 22.04 LTS Storage Setup

Ubuntu 22.04 LTS (Jammy Jellyfish) provides excellent storage capabilities out of the box. This section covers the complete setup and configuration process for optimal storage management.

### System Requirements and Preparation

#### Minimum System Requirements

```text

    Component          | Minimum         | Recommended
    -------------------|-----------------|------------------
    RAM                | 4 GB           | 8 GB or more
    Storage            | 25 GB          | 100 GB or more
    CPU                | 2 GHz dual-core| 2 GHz quad-core
    Graphics           | VGA capable    | GPU with driver support

#### Pre-Installation Planning

```bash

    # Check hardware compatibility
    lshw -short
    lscpu
    lsmem
    lsblk

    # Check UEFI/BIOS mode
    [ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"

    # Verify secure boot status
    mokutil --sb-state

### Storage-Focused Installation

Partitioning Strategies
^^^^^^^^^^^^^^^^^^^^^^

**Option 1: Simple Layout (Recommended for most users)**

```text

    Device    | Mount Point | Size      | Filesystem | Purpose
    ----------|-------------|-----------|------------|------------------
    /dev/sda1 | /boot/efi   | 512 MB    | FAT32      | EFI System
    /dev/sda2 | /           | 50-100 GB | ext4       | Root filesystem
    /dev/sda3 | /home       | Remaining | ext4       | User data
    /dev/sda4 | [SWAP]      | 2x RAM    | swap       | Virtual memory

**Option 2: Advanced Layout (For servers/power users)**

```text

    Device    | Mount Point | Size      | Filesystem | Purpose
    ----------|-------------|-----------|------------|------------------
    /dev/sda1 | /boot/efi   | 512 MB    | FAT32      | EFI System
    /dev/sda2 | /boot       | 1 GB      | ext4       | Boot files
    /dev/sda3 | /           | 20 GB     | ext4       | Root filesystem
    /dev/sda4 | /var        | 20 GB     | ext4       | Variable data
    /dev/sda5 | /tmp        | 5 GB      | ext4       | Temporary files
    /dev/sda6 | /home       | Remaining | ext4       | User data
    /dev/sda7 | [SWAP]      | 2x RAM    | swap       | Virtual memory

#### Manual Partitioning with fdisk

```bash

    # Start partitioning
    sudo fdisk /dev/sda

    # Create GPT partition table
    Command: g

    # Create EFI partition
    Command: n
    Partition number: 1
    First sector: (default)
    Last sector: +512M
    Command: t
    Partition type: 1 (EFI System)

    # Create root partition
    Command: n
    Partition number: 2
    First sector: (default)
    Last sector: +50G
    # (ext4 by default)

    # Create home partition
    Command: n
    Partition number: 3
    First sector: (default)
    Last sector: (default - use remaining space)

    # Write changes
    Command: w

#### LVM Setup for Flexible Storage

```bash

    # Install LVM tools
    sudo apt update
    sudo apt install lvm2

    # Create physical volume
    sudo pvcreate /dev/sda3

    # Create volume group
    sudo vgcreate ubuntu-vg /dev/sda3

    # Create logical volumes
    sudo lvcreate -L 20G -n root ubuntu-vg
    sudo lvcreate -L 10G -n var ubuntu-vg
    sudo lvcreate -L 5G -n tmp ubuntu-vg
    sudo lvcreate -l 100%FREE -n home ubuntu-vg

    # Format logical volumes
    sudo mkfs.ext4 /dev/ubuntu-vg/root
    sudo mkfs.ext4 /dev/ubuntu-vg/var
    sudo mkfs.ext4 /dev/ubuntu-vg/tmp
    sudo mkfs.ext4 /dev/ubuntu-vg/home

Post-Installation Storage Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Update System and Install Essential Tools

```bash

    # Update package lists and system
    sudo apt update && sudo apt upgrade -y

    # Install essential storage tools
    sudo apt install -y \\
        gdisk \\
        parted \\
        gparted \\
        lvm2 \\
        mdadm \\
        smartmontools \\
        hdparm \\
        iotop \\
        htop \\
        tree \\
        ncdu \\
        rsync \\
        rclone \\
        fdupes \\
        testdisk \\
        ddrescue \\
        safecopy

    # Install filesystem tools
    sudo apt install -y \\
        xfsprogs \\
        btrfs-progs \\
        ntfs-3g \\
        exfat-fuse \\
        exfat-utils

#### Configure Storage Monitoring

```bash

    # Enable and configure SMART monitoring
    sudo systemctl enable smartmontools
    sudo systemctl start smartmontools

    # Configure smartd
    sudo nano /etc/smartd.conf
    # Add: /dev/sda -a -o on -S on -s (S/../.././02|L/../../6/03)

    # Enable automatic TRIM for SSDs
    sudo systemctl enable fstrim.timer
    sudo systemctl start fstrim.timer

    # Verify TRIM is working
    sudo fstrim -v /

Optimize Storage Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

```bash

    # Check current I/O scheduler
    cat /sys/block/sda/queue/scheduler

    # Set optimal I/O scheduler for SSDs
    echo none | sudo tee /sys/block/sda/queue/scheduler

    # Set optimal I/O scheduler for HDDs
    echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler

    # Make scheduler change permanent
    echo 'ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="none"' | sudo tee /etc/udev/rules.d/60-ioschedulers.rules
    echo 'ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="mq-deadline"' | sudo tee -a /etc/udev/rules.d/60-ioschedulers.rules

Storage Security Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Full Disk Encryption with LUKS

```bash

    # Install cryptsetup
    sudo apt install cryptsetup

    # Encrypt a partition
    sudo cryptsetup luksFormat /dev/sdb1

    # Open encrypted partition
    sudo cryptsetup luksOpen /dev/sdb1 encrypted_drive

    # Create filesystem on encrypted partition
    sudo mkfs.ext4 /dev/mapper/encrypted_drive

    # Mount encrypted partition
    sudo mkdir /mnt/encrypted
    sudo mount /dev/mapper/encrypted_drive /mnt/encrypted

    # Add to /etc/crypttab for automatic mounting
    echo "encrypted_drive /dev/sdb1 none luks" | sudo tee -a /etc/crypttab

    # Add to /etc/fstab
    echo "/dev/mapper/encrypted_drive /mnt/encrypted ext4 defaults 0 2" | sudo tee -a /etc/fstab

File Permissions and Access Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```bash

    # Set up secure permissions for user data
    sudo chmod 750 /home/username
    sudo chown username:username /home/username

    # Create shared directories with proper permissions
    sudo mkdir /shared
    sudo chown root:users /shared
    sudo chmod 2775 /shared

    # Set up ACLs for fine-grained control
    sudo apt install acl

    # Example: Give user read/write access to specific directory
    sudo setfacl -m u:username:rw /path/to/directory
    sudo setfacl -m g:groupname:r /path/to/directory

### Backup and Recovery Setup

#### Automated Backup Configuration

```bash

    # Create backup directories
    sudo mkdir -p /backup/{daily,weekly,monthly}
    sudo mkdir -p /backup/system/{etc,home,var}

    # Install backup tools
    sudo apt install rsync borgbackup duplicity

    # Create backup script
    cat > /usr/local/bin/backup_system.sh << 'EOF'
    #!/bin/bash
    
    BACKUP_DIR="/backup"
    DATE=$(date +%Y%m%d_%H%M%S)
    LOG_FILE="/var/log/backup.log"
    
    log_message() {
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
    }
    
    # Backup system configuration
    backup_system() {
        log_message "Starting system backup"
        
        # Backup /etc
        rsync -av /etc/ "$BACKUP_DIR/system/etc/"
        
        # Backup user homes
        rsync -av /home/ "$BACKUP_DIR/system/home/" --exclude=".cache"
        
        # Backup important /var directories
        rsync -av /var/log/ "$BACKUP_DIR/system/var/log/"
        rsync -av /var/lib/dpkg/ "$BACKUP_DIR/system/var/lib/dpkg/"
        
        log_message "System backup completed"
    }
    
    # Backup user data
    backup_data() {
        log_message "Starting data backup"
        
        for user_dir in /home/*; do
            if [ -d "$user_dir" ]; then
                username=$(basename "$user_dir")
                rsync -av "$user_dir/" "$BACKUP_DIR/daily/$username/" \\
                    --exclude=".cache" \\
                    --exclude=".thumbnails" \\
                    --exclude="Downloads"
            fi
        done
        
        log_message "Data backup completed"
    }
    
    # Create compressed archive
    create_archive() {
        log_message "Creating compressed archive"
        
        tar -czf "$BACKUP_DIR/archive/backup_$DATE.tar.gz" \\
            -C "$BACKUP_DIR" daily system
        
        # Remove archives older than 30 days
        find "$BACKUP_DIR/archive" -name "*.tar.gz" -mtime +30 -delete
        
        log_message "Archive created: backup_$DATE.tar.gz"
    }
    
    # Main execution
    mkdir -p "$BACKUP_DIR/archive"
    backup_system
    backup_data
    create_archive
    
    # Send notification
    echo "Backup completed on $(hostname) at $(date)" | \\
        mail -s "Backup Report" admin@localhost 2>/dev/null || true
    EOF

    chmod +x /usr/local/bin/backup_system.sh

    # Schedule backup with cron
    echo "0 2 * * * /usr/local/bin/backup_system.sh" | sudo crontab -

### Storage Monitoring and Alerts

#### System Health Monitoring

```bash

    # Create monitoring script
    cat > /usr/local/bin/storage_monitor.sh << 'EOF'
    #!/bin/bash
    
    LOG_FILE="/var/log/storage_monitor.log"
    ALERT_THRESHOLD=85
    SMART_LOG="/var/log/smart_check.log"
    
    log_message() {
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
    }
    
    # Check disk usage
    check_disk_usage() {
        log_message "Checking disk usage"
        
        df -h | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{print $5 " " $1 " " $6}' | while read usage device mount; do
            usage_percent=$(echo $usage | sed 's/%//g')
            
            if [ $usage_percent -ge $ALERT_THRESHOLD ]; then
                log_message "ALERT: $device ($mount) is ${usage_percent}% full"
                echo "Disk usage alert: $device ($mount) is ${usage_percent}% full" | \\
                    mail -s "Disk Usage Alert - $(hostname)" admin@localhost
            fi
        done
    }
    
    # Check SMART status
    check_smart_status() {
        log_message "Checking SMART status"
        
        for device in /dev/sd[a-z]; do
            if [ -b "$device" ]; then
                smart_status=$(smartctl -H "$device" 2>/dev/null | grep "SMART overall-health" | awk '{print $6}')
                
                if [ "$smart_status" = "PASSED" ]; then
                    log_message "$device: SMART status OK"
                elif [ "$smart_status" = "FAILED" ]; then
                    log_message "ALERT: $device SMART status FAILED"
                    echo "SMART failure detected on $device" | \\
                        mail -s "SMART Failure Alert - $(hostname)" admin@localhost
                fi
                
                # Log detailed SMART info
                smartctl -a "$device" >> "$SMART_LOG"
            fi
        done
    }
    
    # Check filesystem errors
    check_filesystem_errors() {
        log_message "Checking filesystem errors"
        
        # Check dmesg for filesystem errors
        if dmesg | grep -i "error\|fault\|fail" | grep -i "ext4\|xfs\|btrfs" > /dev/null; then
            log_message "ALERT: Filesystem errors detected in dmesg"
            dmesg | grep -i "error\|fault\|fail" | grep -i "ext4\|xfs\|btrfs" | \\
                mail -s "Filesystem Error Alert - $(hostname)" admin@localhost
        fi
    }
    
    # Check RAID status (if applicable)
    check_raid_status() {
        if [ -f /proc/mdstat ]; then
            log_message "Checking RAID status"
            
            if grep -q "_" /proc/mdstat; then
                log_message "ALERT: RAID degraded state detected"
                cat /proc/mdstat | mail -s "RAID Alert - $(hostname)" admin@localhost
            fi
        fi
    }
    
    # Main execution
    check_disk_usage
    check_smart_status
    check_filesystem_errors
    check_raid_status
    
    log_message "Storage monitoring completed"
    EOF

    chmod +x /usr/local/bin/storage_monitor.sh

    # Schedule monitoring
    echo "0 */6 * * * /usr/local/bin/storage_monitor.sh" | sudo crontab -

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~

#### Kernel Parameter Tuning

```bash

    # Create performance tuning configuration
    cat > /etc/sysctl.d/99-storage-performance.conf << 'EOF'
    # Storage performance optimizations
    
    # Increase dirty page writeback interval
    vm.dirty_writeback_centisecs = 500
    
    # Increase dirty page ratio
    vm.dirty_ratio = 20
    vm.dirty_background_ratio = 10
    
    # Optimize memory management
    vm.swappiness = 10
    vm.vfs_cache_pressure = 50
    
    # Increase inotify limits
    fs.inotify.max_user_watches = 524288
    fs.inotify.max_user_instances = 256
    
    # Optimize network buffer sizes (for network storage)
    net.core.rmem_max = 134217728
    net.core.wmem_max = 134217728
    EOF

    # Apply settings
    sudo sysctl -p /etc/sysctl.d/99-storage-performance.conf

#### Mount Options Optimization

```bash

    # Optimize /etc/fstab for performance
    sudo cp /etc/fstab /etc/fstab.backup

    # Example optimized fstab entries
    cat >> /etc/fstab << 'EOF'
    # Optimized mount options
    # SSD mounts with noatime and discard
    UUID=your-ssd-uuid /home ext4 defaults,noatime,discard 0 2

    # HDD mounts with relatime
    UUID=your-hdd-uuid /data ext4 defaults,relatime 0 2

    # Temporary filesystems in RAM
    tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=2G 0 0
    tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=1G 0 0
    EOF

Frequently Asked Questions
~~~~~~~~~~~~~~~~~~~~~~~~~

#### Q: How do I check if my system is using UEFI or BIOS?

**A:** Use these commands to determine your boot mode:

```bash

    # Check for UEFI
    [ -d /sys/firmware/efi ] && echo "UEFI boot" || echo "BIOS boot"

    # Check boot mode in more detail
    bootctl status

    # List EFI variables (UEFI only)
    efibootmgr -v

Q: What filesystem should I use for different use cases?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**A:** Recommended filesystems by use case:

```text

    Use Case                | Recommended Filesystem | Reason
    ------------------------|------------------------|------------------
    Root partition (/)      | ext4                  | Stable, well-tested
    Boot partition (/boot)  | ext4                  | Simple, reliable
    Home directories        | ext4                  | Good performance
    Large files/media       | XFS                   | Better large file handling
    Snapshots needed        | Btrfs                 | Built-in snapshots
    Windows compatibility   | NTFS                  | Cross-platform access
    USB drives             | exFAT                 | Universal compatibility

#### Q: How do I resize partitions safely in Ubuntu 22.04?

**A:** Follow these steps for safe partition resizing:

```bash

    # 1. BACKUP YOUR DATA FIRST!

    # 2. For ext4 filesystems:
    # Unmount the partition
    sudo umount /dev/sda2

    # Check filesystem
    sudo fsck -f /dev/sda2

    # Resize partition with parted
    sudo parted /dev/sda resizepart 2 100%

    # Resize filesystem to match partition
    sudo resize2fs /dev/sda2

    # 3. For LVM volumes:
    # Extend physical volume
    sudo pvresize /dev/sda3

    # Extend logical volume
    sudo lvextend -l +100%FREE /dev/ubuntu-vg/home

    # Resize filesystem
    sudo resize2fs /dev/ubuntu-vg/home

Q: How do I set up automatic mounting for external drives?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**A:** Configure automatic mounting:

```bash

    # 1. Get device UUID
    sudo blkid /dev/sdb1

    # 2. Create mount point
    sudo mkdir /mnt/external

    # 3. Add to fstab
    echo "UUID=your-device-uuid /mnt/external ext4 defaults,user,noauto 0 0" | sudo tee -a /etc/fstab

    # 4. Test mounting
    mount /mnt/external

    # 5. For auto-mount on insertion (using udev rules)
    cat > /etc/udev/rules.d/99-usb-mount.rules << 'EOF'
    # Auto-mount USB drives
    KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/usr/local/bin/usb-mount.sh %k"
    KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/usr/local/bin/usb-unmount.sh %k"
    EOF

Troubleshooting Common Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Boot Issues

```bash

    # Repair GRUB bootloader
    sudo grub-install /dev/sda
    sudo update-grub

    # Boot from live USB and repair
    sudo mount /dev/sda2 /mnt
    sudo mount /dev/sda1 /mnt/boot/efi
    sudo mount --bind /dev /mnt/dev
    sudo mount --bind /proc /mnt/proc
    sudo mount --bind /sys /mnt/sys
    sudo chroot /mnt
    grub-install /dev/sda
    update-grub
    exit

#### Filesystem Corruption

```bash

    # Check and repair ext4 filesystem
    sudo fsck.ext4 -f /dev/sda2

    # For automatic repair
    sudo fsck.ext4 -p /dev/sda2

    # For interactive repair
    sudo fsck.ext4 /dev/sda2

    # Check XFS filesystem
    sudo xfs_check /dev/sda2

    # Repair XFS filesystem
    sudo xfs_repair /dev/sda2

#### Disk Space Issues

```bash

    # Find large files
    sudo find / -type f -size +100M -exec ls -lh {} \\; | awk '{print $9 ": " $5}'

    # Clean package cache
    sudo apt autoclean
    sudo apt autoremove

    # Clean logs
    sudo journalctl --vacuum-time=7d

    # Clean thumbnails and cache
    rm -rf ~/.cache/thumbnails/*
    rm -rf ~/.cache/*

Performance Issues
^^^^^^^^^^^^^^^^^

```bash

    # Check I/O wait
    iostat -x 1

    # Monitor disk activity
    sudo iotop

    # Check for filesystem errors
    dmesg | grep -i error

    # Analyze slow queries (for databases)
    sudo apt install sysstat
    sar -d 1 10

```

---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---