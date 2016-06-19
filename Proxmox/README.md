## SYSLINUX

### Proxmox 3

```
LABEL Proxmox_3
    MENU LABEL Proxmox 3
    LINUX images/proxmox/linux26
    INITRD images/proxmox/initrd.img splash=verbose
    APPEND vga=791 video=vesafb:ywrap,mtrr ramdisk_size=16777216
```

### Proxmox 4

```
LABEL Proxmox_4
    MENU LABEL Proxmox 4
    LINUX images/proxmox/linux26
    INITRD images/proxmox/initrd.img
    APPEND root=/dev/ram0 vga=791 ramdisk_size=16777216 quiet splash=verbose
```
