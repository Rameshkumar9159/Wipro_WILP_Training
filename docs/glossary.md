# Name: T S Rameshkumar 
# Batch: WiproNGA_Datacentre_B9_25VID2182

# Glossary

This glossary provides definitions for storage-related terms and concepts used throughout this documentation.

.. glossary::

   AHCI
      Advanced Host Controller Interface - A technical standard for SATA host controllers that allows software to communicate with storage devices.

   Block Device
      A type of device that provides buffered access to hardware devices, allowing data to be read and written in fixed-size blocks (typically 512 bytes or 4096 bytes).

   Block Size
      The minimum unit of data that a filesystem can allocate. Common block sizes are 4KB, 8KB, and 64KB. Larger block sizes are better for sequential access, while smaller block sizes are more efficient for random access.

   BTRFS
      B-Tree File System - A modern filesystem for Linux that features snapshots, checksums, compression, and advanced volume management capabilities.

   Cache
      High-speed storage used to temporarily store frequently accessed data to improve performance. Can be implemented in hardware (disk cache) or software (filesystem cache).

   CIFS
      Common Internet File System - A network protocol used for sharing files, printers, and other resources between systems, primarily used with Windows networks.

   DAS
      Direct-Attached Storage - Storage devices directly connected to a single computer without a network connection, such as internal hard drives or external USB drives.

   Defragmentation
      The process of reorganizing data on a storage device to reduce fragmentation and improve performance. Less relevant for modern filesystems and SSDs.

   Device Mapper
      A Linux kernel framework that provides a generic way to create virtual layers on top of block devices, used by LVM and device encryption.

   Dirty Pages
      Memory pages that have been modified but not yet written to storage. The kernel manages when these pages are flushed to disk.

   DM-Crypt
      Device-mapper crypt target - A Linux kernel module that provides transparent encryption of block devices using the device mapper infrastructure.

   ECC
      Error-Correcting Code - Technology that detects and corrects data corruption errors in memory and storage systems.

   Ext4
      Fourth Extended Filesystem - The default filesystem for many Linux distributions, offering journaling, large file support, and backward compatibility.

   Filesystem
      A method of organizing and storing data on storage devices. Examples include ext4, XFS, NTFS, and APFS.

   FSTAB
      File Systems Table - A configuration file (/etc/fstab) that defines how disk partitions and storage devices should be mounted at boot time.

   GPT
      GUID Partition Table - A modern partitioning scheme that replaces MBR, supporting larger disks and more partitions.

   HDD
      Hard Disk Drive - Traditional storage device using spinning magnetic disks and mechanical read/write heads.

   Hot Spare
      A standby disk in a RAID array that automatically replaces a failed disk without manual intervention.

   I/O
      Input/Output - Operations that transfer data between the computer and storage devices or other external systems.

   Inode
      Index node - A data structure that stores metadata about files and directories in Unix-like filesystems, including permissions, timestamps, and pointers to data blocks.

   IOPS
      Input/Output Operations Per Second - A performance measurement indicating how many read/write operations a storage device can perform per second.

   iSCSI
      Internet Small Computer Systems Interface - A protocol that allows SCSI commands to be sent over IP networks, enabling network-attached storage.

   Journal
      A log of filesystem changes used for crash recovery. Journaling filesystems can quickly recover from unexpected shutdowns by replaying the journal.

   JBOD
      Just a Bunch of Disks - A storage configuration where multiple disks are used independently without RAID redundancy.

   LBA
      Logical Block Addressing - A method of addressing data blocks on storage devices using a linear sequence of block numbers.

   Logical Volume
      A virtual storage device created by LVM that can span multiple physical devices and be resized dynamically.

   LUKS
      Linux Unified Key Setup - A disk encryption specification and reference implementation for Linux that provides a standard format for encrypted storage.

   LUN
      Logical Unit Number - A number used to identify individual devices or logical units within a SCSI target.

   LVM
      Logical Volume Manager - A system for managing disk space that provides volume management capabilities including resizing, snapshots, and spanning multiple devices.

   MBR
      Master Boot Record - An older partitioning scheme limited to 2TB disks and 4 primary partitions.

   mdadm
      Multiple Device Administration - A Linux utility for managing software RAID arrays.

   Mount Point
      A directory in the filesystem hierarchy where a storage device or filesystem is attached and made accessible.

   NAS
      Network-Attached Storage - File-level storage accessible over a network, typically using protocols like NFS or SMB/CIFS.

   NFS
      Network File System - A protocol for sharing files over a network, allowing remote directories to be mounted as if they were local.

   NVME
      Non-Volatile Memory Express - A high-performance interface for SSDs that connects directly to the CPU via PCIe lanes.

   Partition
      A logical division of a storage device that appears to the operating system as a separate device.

   Physical Extent
      The smallest unit of space allocation in LVM, typically 4MB in size.

   Physical Volume
      A storage device or partition that has been initialized for use with LVM.

   RAID
      Redundant Array of Independent Disks - A technology that combines multiple physical disks into logical units for redundancy, performance, or both.

   RAID 0
      Disk striping without redundancy - improves performance but provides no fault tolerance.

   RAID 1
      Disk mirroring - provides redundancy by maintaining identical copies of data on multiple disks.

   RAID 5
      Distributed parity - requires minimum 3 disks, provides redundancy and improved read performance.

   RAID 6
      Double distributed parity - requires minimum 4 disks, can tolerate failure of any two disks.

   RAID 10
      Combination of RAID 1 and RAID 0 - provides both redundancy and performance improvements.

   RPO
      Recovery Point Objective - The maximum acceptable amount of data loss measured in time (e.g., 1 hour RPO means losing at most 1 hour of data).

   RTO
      Recovery Time Objective - The maximum acceptable time to restore service after a failure (e.g., 4 hour RTO means service must be restored within 4 hours).

   SAN
      Storage Area Network - A dedicated high-speed network that provides block-level access to storage devices.

   SATA
      Serial Advanced Technology Attachment - A computer bus interface for connecting storage devices like hard drives and SSDs.

   SCSI
      Small Computer System Interface - A set of standards for connecting and transferring data between computers and storage devices.

   Sector
      The smallest addressable unit on a storage device, traditionally 512 bytes but increasingly 4096 bytes (4K sectors).

   SMART
      Self-Monitoring, Analysis and Reporting Technology - A monitoring system for storage devices that detects and reports various reliability indicators.

   Snapshot
      A point-in-time copy of a filesystem or volume that captures the state of data at a specific moment, useful for backups and recovery.

   SSD
      Solid State Drive - Storage device using NAND flash memory with no moving parts, offering better performance and reliability than HDDs.

   Swap
      Virtual memory space on storage devices used when physical RAM is insufficient. Also called a page file.

   Throughput
      The amount of data transferred per unit of time, typically measured in MB/s or GB/s.

   TRIM
      A command that informs SSDs which data blocks are no longer needed, allowing the drive to optimize performance and wear leveling.

   UUID
      Universally Unique Identifier - A 128-bit identifier used to uniquely identify storage devices and filesystems.

   Volume Group
      A collection of physical volumes in LVM that provides a pool of storage space for creating logical volumes.

   Wear Leveling
      A technique used in SSDs to distribute write operations evenly across memory cells to maximize device lifespan.

   XFS
      A high-performance journaling filesystem originally developed for IRIX, known for excellent scalability and large file support.

   ZFS
      Zettabyte File System - An advanced filesystem and volume manager that provides features like checksums, compression, snapshots, and data deduplication.

# Common Command Abbreviations

.. glossary::

   blkid
      Block device identifier - Command to display information about block devices and their attributes.

   dd
      Data duplicator (historically "disk dump") - Command for copying and converting raw data between devices.

   df
      Disk free - Command to display filesystem disk space usage.

   du
      Disk usage - Command to display directory space usage.

   fdisk
      Fixed disk - Partition table manipulator for MBR partitions.

   fsck
      File system check - Command to check and repair filesystem errors.

   gdisk
      GPT fdisk - Partition table manipulator for GPT partitions.

   lsblk
      List block devices - Command to display block device information in tree format.

   mount
      Mount filesystem - Command to attach filesystems to the directory tree.

   parted
      Partition editor - Command-line tool for creating and manipulating partition tables.

   rsync
      Remote sync - Command for efficiently synchronizing files and directories.

   umount
      Unmount filesystem - Command to detach filesystems from the directory tree.

Storage Unit Definitions
=======================

.. glossary::

   Byte
      The basic unit of digital information, consisting of 8 bits.

   KB (Kilobyte)
      1,000 bytes (decimal) or 1,024 bytes (binary, more precisely called KiB).

   MB (Megabyte)
      1,000,000 bytes (decimal) or 1,048,576 bytes (binary, more precisely called MiB).

   GB (Gigabyte)
      1,000,000,000 bytes (decimal) or 1,073,741,824 bytes (binary, more precisely called GiB).

   TB (Terabyte)
      1,000,000,000,000 bytes (decimal) or 1,099,511,627,776 bytes (binary, more precisely called TiB).

   PB (Petabyte)
      1,000,000,000,000,000 bytes (decimal) or 1,125,899,906,842,624 bytes (binary, more precisely called PiB).

# Performance Metrics

.. glossary::

   Bandwidth
      The maximum data transfer rate of a storage system, typically measured in MB/s or GB/s.

   Latency
      The time delay between when a storage operation is requested and when it begins, typically measured in milliseconds.

   Queue Depth
      The number of pending I/O operations that can be queued for processing by a storage device.

   Random I/O
      Storage operations that access data at non-sequential locations, typically slower than sequential I/O.

   Sequential I/O
      Storage operations that access data in a continuous, ordered manner, typically faster than random I/O.

   Sustained Transfer Rate
      The average data transfer rate over an extended period, excluding burst performance.

RAID Levels Reference
====================

.. glossary::

   RAID 0
      Striping - Data is split across multiple drives for improved performance. No redundancy. Minimum 2 drives.

   RAID 1
      Mirroring - Data is duplicated across drives for redundancy. 50% storage efficiency. Minimum 2 drives.

   RAID 5
      Distributed parity - Data and parity information spread across all drives. Can lose 1 drive. Minimum 3 drives.

   RAID 6
      Double parity - Two parity blocks per stripe. Can lose 2 drives. Minimum 4 drives.

   RAID 10
      Mirror of stripes - Combines RAID 1 and RAID 0. High performance and redundancy. Minimum 4 drives.

   RAID 50
      Striped RAID 5 - Multiple RAID 5 arrays striped together. Minimum 6 drives.

   RAID 60
      Striped RAID 6 - Multiple RAID 6 arrays striped together. Minimum 8 drives.

# Network Storage Protocols

.. glossary::

   AFP
      Apple Filing Protocol - Network protocol for file sharing used primarily by Apple devices.

   FTP
      File Transfer Protocol - Standard protocol for transferring files over networks.

   HTTP/HTTPS
      Hypertext Transfer Protocol - Web protocol that can also be used for file access via WebDAV.

   NFS v3
      Network File System version 3 - Stateless file sharing protocol, widely supported.

   NFS v4
      Network File System version 4 - Stateful protocol with improved security and features.

   SFTP
      SSH File Transfer Protocol - Secure file transfer protocol that operates over SSH.

   SMB/CIFS
      Server Message Block / Common Internet File System - File sharing protocol used primarily in Windows environments.

   WebDAV
      Web Distributed Authoring and Versioning - Extension to HTTP for collaborative file management.

File System Features
===================

.. glossary::

   Compression
      Feature that reduces file size by encoding data more efficiently, saving storage space at the cost of CPU overhead.

   Copy-on-Write
      Technique where data is not physically copied until it is modified, used in snapshots and some filesystems.

   Deduplication
      Process of eliminating duplicate data to reduce storage requirements.

   Encryption
      Process of encoding data to prevent unauthorized access, can be implemented at filesystem or block device level.

   Journaling
      Technique that logs filesystem changes before committing them, enabling fast recovery after crashes.

   Quotas
      Limits placed on storage usage by users or groups to prevent overconsumption of disk space.

   Snapshots
      Point-in-time copies of filesystem state that can be used for backups or recovery.

   Sparse Files
      Files that contain large blocks of zero bytes that are not actually stored on disk, saving space.

This glossary provides essential terminology for understanding storage concepts in Ubuntu 22.04 and serves as a quick reference for technical terms used throughout the documentation.


---
Name: T S Rameshkumar <rameshsv06@gmail.com>  
Batch: WiproNGA_Datacentre_B9_25VID2182
---