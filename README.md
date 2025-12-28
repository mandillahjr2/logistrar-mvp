# IP Monitor MVP

A simple cybersecurity tool for monitoring network traffic and flagging unknown IP addresses.

## Features

- Reads router traffic logs (syslog format)
- Maintains a list of known/trusted IPs and subnets
- Flags any traffic involving unknown IPs
- Simple console alerts
- Supports continuous monitoring (like `tail -f`)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ip-monitor-mvp.git
cd ip-monitor-mvp

# No dependencies required (uses Python standard library)
```


# Basic usage

python monitor.py -f traffic.log -k known_ips.txt

## Continuous monitoring

python monitor.py -f /var/log/syslog -t -k known_ips.txt

## File Structure

* `monitor.py` - Main monitoring script
* `known_ips.txt` - List of trusted IPs/subnets
* `traffic.log` - Sample traffic logs
* `.gitignore` - Git ignore file

## Configuration

Add your trusted IPs to `known_ips.txt`:
