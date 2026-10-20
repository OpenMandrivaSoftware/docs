---
layout: default
title: Network Configuration
nav_order: 50
parent: User Guide
has_toc: true
lang: en
---
# Network Configuration

OpenMandriva Lx provides tools to configure and manage network connections. This guide covers graphical and command-line methods.

## Graphical Network Configuration

Use these methods to set up and manage network connections through a graphical interface.

### NetworkManager

OpenMandriva uses NetworkManager to manage connections. Click the network icon in the system tray to access it.

1. Click the network icon in the system tray
1. Select *Edit Connections...*
1. Choose the connection to configure, or click *+* to create a new one
1. Configure settings (IPv4, IPv6, DNS, etc.)
1. Click *Save*

### Plasma Network Management

For KDE Plasma users, access additional network settings through

- **System Settings** → **Network** → **Connections**
- Or run `kcmshell5 kcm_networkmanager` from the terminal

## Command-Line Network Configuration

Use these tools to manage connections from the terminal.

### Using `nmcli`

`nmcli` (NetworkManager Command Line Interface) manages connections from the terminal.

```bash
# List available connections
nmcli connection show

# List active connections
nmcli device status

# Create a new connection
nmcli connection add type ethernet ifname eth0

# Modify a connection
nmcli connection modify "Connection Name" ipv4.addresses "192.168.1.100/24"

# Activate a connection
nmcli connection up "Connection Name"

# Deactivate a connection
nmcli connection down "Connection Name"
```

### Using `nmtui`

`nmtui` (Ninja Text User Interface) provides a text-based interface for NetworkManager:

```bash
nmtui
```

This opens an interactive menu for configuring

- Editing connections
- Activating and deactivating connections
- Setting up bonding, VLANs, and tunnels

### Using the `ip` Command

For basic network configuration, use the `ip` command:

```bash
# Show network interfaces
ip addr show

# Bring up an interface
ip link set dev eth0 up

# Assign an IP address
ip addr add 192.168.1.100/24 dev eth0

# Set default gateway
ip route add default via 192.168.1.1
```

## Wi-Fi Configuration

Configure wireless connections using these methods.

### Graphical Method

1. Click the network icon in the system tray
1. Select a Wi-Fi network from the list
1. Enter the password when prompted
1. Check *Remember this network* if desired

### Command-Line Method

```bash
# List available Wi-Fi networks
nmcli device wifi list

# Connect to a Wi-Fi network
nmcli device wifi connect "SSID" password "password"

# Scan for networks
nmcli device wifi rescan
```

## Troubleshooting

Resolve common network issues with these diagnostic steps.

### Check Network Status

Run these commands to diagnose network problems:

```bash
# Check if network interface is up
ip link show

# Check IP addresses assigned
ip addr show

# Check routing table
ip route show

# Check DNS configuration
cat /etc/resolv.conf
```

### Common Issues

**No network connection after boot:**
- Check if the network interface is enabled: `nmcli device status`
- Restart NetworkManager: `systemctl restart NetworkManager`

**Can't resolve domain names:**
- Check DNS settings in `/etc/resolv.conf`
- Use `dnssec-trigger` if DNS issues persist

**Wi-Fi not showing available networks:**
- Bring up the interface: `ip link set wlan0 up`
- Check if the wireless adapter is recognized: `lspci | grep -i wireless`

## Advanced Configuration

Configure complex networking setups with these tools.

### Bonding (Link Aggregation)

Create bonded interfaces for increased throughput and redundancy:

```bash
nmcli connection add type bond ifname bond0 mode active-backup
nmcli connection add type ethernetSlave ifname eth0 MASTER bond0
nmcli connection add type ethernetSlave ifname eth1 MASTER bond0
nmcli connection up bond0
```

### VLAN Configuration

Create VLAN interfaces to segment network traffic on specific tags:

```bash
nmcli connection add type vlan con-name vlan10 dev eth0 id 10
nmcli connection modify vlan10 ipv4.addresses "192.168.10.1/24"
nmcli connection up vlan10
```

### Bridge Configuration

Create a bridge for virtualization or container networking:

```bash
nmcli connection add type bridge ifname br0
nmcli connection add type bridge-slave ifname eth0 master br0
nmcli connection modify br0 ipv4.addresses "192.168.1.1/24"
nmcli connection up br0
```

## Related Topics

- [User Guide](index.en.html)
- [Managing Software](managing-software.en.html)