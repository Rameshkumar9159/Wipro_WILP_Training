# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

# Volume Management

Volume management provides an abstraction layer between physical storage devices and file systems, enabling dynamic storage allocation, resizing, and advanced features like snapshots and encryption.

   :local:
   :depth: 2

## Introduction to Volume Management

Volume management systems allow you to:

* Combine multiple physical disks into logical volumes
* Resize volumes dynamically without downtime
* Create snapshots for backup and testing
* Implement storage encryption and compression
* Manage storage pools efficiently

### Key Concepts

**Physical Volumes (PV)**
  Physical storage devices or partitions

**Volume Groups (VG)**
  Collections of physical volumes

**Logical Volumes (LV)**
  Virtual partitions created from volume groups

**Logical Volume Manager (LVM)**
  The primary volume management system in Linux

## LVM (Logical Volume Manager)

### Installation and Setup

```bash

   # Install LVM tools on Ubuntu 22.04
   sudo apt update
   sudo apt install lvm2

   # Check LVM installation
   lvm version

### Creating Physical Volumes

```bash

   # Create physical volume from disk
   sudo pvcreate /dev/sdb

   # Create PV from partition
   sudo pvcreate /dev/sdc1

   # Display physical volumes
   sudo pvdisplay
   sudo pvs

### Creating Volume Groups

```bash

   # Create volume group from single PV
   sudo vgcreate myvg /dev/sdb

   # Create VG from multiple PVs
   sudo vgcreate datavg /dev/sdb /dev/sdc

   # Display volume groups
   sudo vgdisplay
   sudo vgs

### Creating Logical Volumes

```bash

   # Create LV with specific size
   sudo lvcreate -L 10G -n mylv myvg

   # Create LV using percentage of VG
   sudo lvcreate -l 50%VG -n datalv datavg

   # Create LV using all available space
   sudo lvcreate -l 100%FREE -n homelv myvg

   # Display logical volumes
   sudo lvdisplay
   sudo lvs

### Formatting and Mounting LVM Volumes

```bash

   # Format logical volume
   sudo mkfs.ext4 /dev/myvg/mylv

   # Create mount point
   sudo mkdir /mnt/mylv

   # Mount the volume
   sudo mount /dev/myvg/mylv /mnt/mylv

   # Add to /etc/fstab for persistent mounting
   echo "/dev/myvg/mylv /mnt/mylv ext4 defaults 0 2" | sudo tee -a /etc/fstab

### Resizing LVM Volumes

**Extending Logical Volumes**

```bash

   # Extend LV size
   sudo lvextend -L +5G /dev/myvg/mylv

   # Extend LV to use all available space
   sudo lvextend -l +100%FREE /dev/myvg/mylv

   # Resize filesystem (ext4)
   sudo resize2fs /dev/myvg/mylv

   # For XFS filesystem
   sudo xfs_growfs /mnt/mylv

**Shrinking Logical Volumes**

```bash

   # Unmount the filesystem first
   sudo umount /mnt/mylv

   # Check filesystem
   sudo e2fsck -f /dev/myvg/mylv

   # Shrink filesystem first
   sudo resize2fs /dev/myvg/mylv 8G

   # Then shrink the logical volume
   sudo lvreduce -L 8G /dev/myvg/mylv

   # Remount
   sudo mount /dev/myvg/mylv /mnt/mylv

### LVM Snapshots

```bash

   # Create snapshot
   sudo lvcreate -L 2G -s -n mylv_snapshot /dev/myvg/mylv

   # Mount snapshot for backup
   sudo mkdir /mnt/snapshot
   sudo mount /dev/myvg/mylv_snapshot /mnt/snapshot

   # Remove snapshot after backup
   sudo umount /mnt/snapshot
   sudo lvremove /dev/myvg/mylv_snapshot

### Advanced LVM Features

**LVM Thin Provisioning**

```bash

   # Create thin pool
   sudo lvcreate -L 50G --thinpool mythinpool myvg

   # Create thin volume
   sudo lvcreate -V 100G --thin myvg/mythinpool -n thinlv

   # Monitor thin pool usage
   sudo lvs -o +data_percent,metadata_percent

**LVM Caching**

```bash

   # Create cache pool (requires SSD)
   sudo lvcreate -L 10G -n cachepool myvg /dev/nvme0n1p1

   # Convert to cache pool
   sudo lvconvert --type cache-pool myvg/cachepool

   # Cache a logical volume
   sudo lvconvert --type cache --cachepool myvg/cachepool myvg/mylv

## ZFS Volume Management

### Installation on Ubuntu 22.04

```bash

   # Install ZFS
   sudo apt install zfsutils-linux

   # Load ZFS module
   sudo modprobe zfs

   # Verify installation
   zfs version

### Creating ZFS Pools

```bash

   # Create simple pool
   sudo zpool create mypool /dev/sdb

   # Create mirrored pool
   sudo zpool create mypool mirror /dev/sdb /dev/sdc

   # Create RAIDZ pool (RAID5-like)
   sudo zpool create mypool raidz /dev/sdb /dev/sdc /dev/sdd

   # Check pool status
   sudo zpool status
   sudo zpool list

### Creating ZFS Datasets

```bash

   # Create dataset
   sudo zfs create mypool/data

   # Create dataset with compression
   sudo zfs create -o compression=lz4 mypool/compressed

   # Set quota
   sudo zfs set quota=10G mypool/data

   # List datasets
   sudo zfs list

### ZFS Snapshots and Clones

```bash

   # Create snapshot
   sudo zfs snapshot mypool/data@backup-$(date +%Y%m%d)

   # List snapshots
   sudo zfs list -t snapshot

   # Clone snapshot
   sudo zfs clone mypool/data@backup-20250715 mypool/data-clone

   # Rollback to snapshot
   sudo zfs rollback mypool/data@backup-20250715

## Btrfs Volume Management

### Creating Btrfs Volumes

```bash

   # Create single device Btrfs
   sudo mkfs.btrfs /dev/sdb

   # Create multi-device Btrfs
   sudo mkfs.btrfs -d raid1 -m raid1 /dev/sdb /dev/sdc

   # Mount Btrfs filesystem
   sudo mount /dev/sdb /mnt/btrfs

### Btrfs Subvolumes

```bash

   # Create subvolume
   sudo btrfs subvolume create /mnt/btrfs/subvol1

   # List subvolumes
   sudo btrfs subvolume list /mnt/btrfs

   # Mount subvolume
   sudo mount -o subvol=subvol1 /dev/sdb /mnt/subvol1

### Btrfs Snapshots

```bash

   # Create snapshot
   sudo btrfs subvolume snapshot /mnt/btrfs/subvol1 /mnt/btrfs/snapshot1

   # Create read-only snapshot
   sudo btrfs subvolume snapshot -r /mnt/btrfs/subvol1 /mnt/btrfs/ro-snapshot

## Volume Management Scripts

### LVM Monitoring Script

```python

   #!/usr/bin/env python3
   """
   LVM Volume Monitoring Script for Ubuntu 22.04
   """
   
   import subprocess
   import json
   import sys
   
   def run_command(cmd):
       """Execute shell command and return output"""
       try:
           result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
           return result.stdout.strip(), result.returncode
       except Exception as e:
           return str(e), 1
   
   def get_pv_info():
       """Get physical volume information"""
       cmd = "sudo pvs --reportformat json"
       output, code = run_command(cmd)
       if code == 0:
           return json.loads(output)
       return {}
   
   def get_vg_info():
       """Get volume group information"""
       cmd = "sudo vgs --reportformat json"
       output, code = run_command(cmd)
       if code == 0:
           return json.loads(output)
       return {}
   
   def get_lv_info():
       """Get logical volume information"""
       cmd = "sudo lvs --reportformat json"
       output, code = run_command(cmd)
       if code == 0:
           return json.loads(output)
       return {}
   
   def check_space_usage():
       """Check for volume groups with high usage"""
       vg_info = get_vg_info()
       alerts = []
       
       if 'report' in vg_info:
           for vg in vg_info['report'][0]['vg']:
               used_percent = float(vg['vg_used_percent'].rstrip('%'))
               if used_percent > 80:
                   alerts.append(f"VG {vg['vg_name']} is {used_percent}% full")
       
       return alerts
   
   def main():
       print("=== LVM Volume Status ===")
       
       # Physical Volumes
       pv_info = get_pv_info()
       if 'report' in pv_info:
           print("\nPhysical Volumes:")
           for pv in pv_info['report'][0]['pv']:
               print(f"  {pv['pv_name']}: {pv['pv_size']} ({pv['pv_used']} used)")
       
       # Volume Groups
       vg_info = get_vg_info()
       if 'report' in vg_info:
           print("\nVolume Groups:")
           for vg in vg_info['report'][0]['vg']:
               print(f"  {vg['vg_name']}: {vg['vg_size']} ({vg['vg_used_percent']} used)")
       
       # Logical Volumes
       lv_info = get_lv_info()
       if 'report' in lv_info:
           print("\nLogical Volumes:")
           for lv in lv_info['report'][0]['lv']:
               print(f"  {lv['lv_name']}: {lv['lv_size']} ({lv['data_percent'] or 'N/A'}% data)")
       
       # Check for alerts
       alerts = check_space_usage()
       if alerts:
           print("\n=== ALERTS ===")
           for alert in alerts:
               print(f"WARNING: {alert}")
   
   if __name__ == "__main__":
       main()

### Automated Backup Script

```bash

   #!/bin/bash
   # LVM Snapshot Backup Script
   
   VOLUME_GROUP="myvg"
   LOGICAL_VOLUME="mylv"
   SNAPSHOT_NAME="${LOGICAL_VOLUME}_backup_$(date +%Y%m%d_%H%M%S)"
   BACKUP_DIR="/backup"
   SNAPSHOT_SIZE="2G"
   
   # Function to log messages
   log_message() {
       echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a /var/log/lvm_backup.log
   }
   
   # Function to cleanup on exit
   cleanup() {
       if [ -n "$SNAPSHOT_CREATED" ]; then
           log_message "Cleaning up snapshot: $SNAPSHOT_NAME"
           sudo umount /mnt/snapshot 2>/dev/null
           sudo lvremove -f /dev/$VOLUME_GROUP/$SNAPSHOT_NAME
       fi
   }
   
   # Set trap for cleanup
   trap cleanup EXIT
   
   # Create snapshot
   log_message "Creating snapshot: $SNAPSHOT_NAME"
   if sudo lvcreate -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME /dev/$VOLUME_GROUP/$LOGICAL_VOLUME; then
       SNAPSHOT_CREATED=1
       log_message "Snapshot created successfully"
   else
       log_message "Failed to create snapshot"
       exit 1
   fi
   
   # Mount snapshot
   sudo mkdir -p /mnt/snapshot
   if sudo mount /dev/$VOLUME_GROUP/$SNAPSHOT_NAME /mnt/snapshot; then
       log_message "Snapshot mounted at /mnt/snapshot"
   else
       log_message "Failed to mount snapshot"
       exit 1
   fi
   
   # Create backup
   BACKUP_FILE="$BACKUP_DIR/backup_${LOGICAL_VOLUME}_$(date +%Y%m%d_%H%M%S).tar.gz"
   log_message "Creating backup: $BACKUP_FILE"
   
   if sudo tar -czf "$BACKUP_FILE" -C /mnt/snapshot .; then
       log_message "Backup completed: $BACKUP_FILE"
       log_message "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
   else
       log_message "Backup failed"
       exit 1
   fi

## Common Tasks and Q&A

**Q: How do I extend a volume group with a new disk?**

A: Add the new disk as a physical volume and extend the volume group:

```bash

   sudo pvcreate /dev/sdd
   sudo vgextend myvg /dev/sdd

**Q: Can I move data between logical volumes?**

A: Yes, use pvmove to migrate data:

```bash

   # Move all data from /dev/sdb to /dev/sdc
   sudo pvmove /dev/sdb /dev/sdc

**Q: How do I remove a disk from LVM?**

A: First move data, then remove:

```bash

   sudo pvmove /dev/sdb
   sudo vgreduce myvg /dev/sdb
   sudo pvremove /dev/sdb

**Q: What's the difference between thick and thin provisioning?**

A: Thick provisioning allocates all space immediately, while thin provisioning allocates space as needed, allowing overcommitment.

**Q: How do I monitor thin pool usage?**

A: Use lvs with additional columns:

```bash

   sudo lvs -o +data_percent,metadata_percent

## Best Practices

1. **Regular Monitoring**
   - Monitor volume group usage
   - Set up alerts for high usage
   - Regular snapshot cleanup

2. **Backup Strategy**
   - Use LVM snapshots for consistent backups
   - Test restore procedures
   - Keep multiple snapshot generations

3. **Performance**
   - Align volumes with underlying storage
   - Use appropriate stripe sizes
   - Consider SSD caching for performance

4. **Security**
   - Use LUKS encryption for sensitive data
   - Implement proper access controls
   - Regular security audits

5. **Disaster Recovery**
   - Document volume group configurations
   - Practice recovery procedures
   - Maintain offsite backups

## See Also

* :doc:`disk-management`
* :doc:`file-systems`
* :doc:`raid-systems`
* :doc:`troubleshooting`

```

---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---