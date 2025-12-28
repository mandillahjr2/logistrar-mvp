#!/usr/bin/env python3
"""
Simple IP Traffic Monitor MVP
Reads router logs and flags unknown IPs
"""

import re
import ipaddress
from datetime import datetime
import time
import sys

class SimpleIPMonitor:
    def __init__(self, known_ips_file='known_ips.txt'):
        """Load known IPs from file"""
        self.known_ips = self.load_known_ips(known_ips_file)
        if self.known_ips is None:
            self.known_ips = []  # Initialize as empty list if None
        print(f"[*] Loaded {len(self.known_ips)} known IPs/subnets")
    
    def load_known_ips(self, filename):
        """Load known IPs from file, supporting both single IPs and subnets"""
        known = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    known.append(line)
            return known  # MAKE SURE TO RETURN THE LIST!
        except FileNotFoundError:
            print(f"[!] Warning: {filename} not found. Starting with empty known IP list.")
            return []  # Return empty list instead of None
        except Exception as e:
            print(f"[!] Error loading {filename}: {e}")
            return []
    
    def is_ip_known(self, ip):
        """Check if an IP is in known list (supports subnets)"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            for known in self.known_ips:
                try:
                    # Check if it's a single IP
                    if '/' not in known:
                        if ip_obj == ipaddress.ip_address(known):
                            return True
                    # Check if it's a subnet
                    else:
                        if ip_obj in ipaddress.ip_network(known, strict=False):
                            return True
                except ValueError:
                    continue  # Skip invalid entries
        except ValueError:
            return False  # Invalid IP
        
        return False
    
    def extract_ips_from_log(self, log_line):
        """Extract IP addresses from a log line"""
        # Simple regex for IP extraction (IPv4)
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, log_line)
        
        # Filter out invalid IPs (like 0.0.0.0 or broadcast)
        valid_ips = []
        for ip in ips:
            try:
                ip_obj = ipaddress.ip_address(ip)
                if not (ip_obj.is_private and ip.startswith('0.')):
                    valid_ips.append(ip)
            except ValueError:
                pass
        
        return valid_ips
    
    def analyze_log_line(self, log_line):
        """Analyze a single log line for unknown IPs"""
        ips = self.extract_ips_from_log(log_line)
        
        alerts = []
        for ip in ips:
            if not self.is_ip_known(ip):
                alerts.append({
                    'ip': ip,
                    'log_line': log_line.strip(),
                    'timestamp': datetime.now().isoformat()
                })
        
        return alerts
    
    def monitor_file(self, log_file, tail=False):
        """Monitor a log file for new entries"""
        print(f"[*] Monitoring {log_file}")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            if tail:
                # For continuous monitoring (like tail -f)
                with open(log_file, 'r') as f:
                    # Go to end of file
                    f.seek(0, 2)
                    
                    while True:
                        line = f.readline()
                        if line:
                            alerts = self.analyze_log_line(line)
                            if alerts:
                                self.alert(alerts)
                        else:
                            time.sleep(0.1)  # Wait for new content
            else:
                # One-time scan of existing logs
                with open(log_file, 'r') as f:
                    for line in f:
                        alerts = self.analyze_log_line(line)
                        if alerts:
                            self.alert(alerts)
                            
        except KeyboardInterrupt:
            print("\n[*] Stopped by user")
        except FileNotFoundError:
            print(f"[!] Error: {log_file} not found")
    
    def alert(self, alerts):
        """Simple console alerting"""
        for alert in alerts:
            print(f"\n[!] ALERT: Unknown IP detected!")
            print(f"    IP: {alert['ip']}")
            print(f"    Time: {alert['timestamp']}")
            print(f"    Log: {alert['log_line'][:100]}...")
            print("-" * 50)

def main():
    # Simple command-line interface
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple IP Traffic Monitor MVP')
    parser.add_argument('-f', '--logfile', default='traffic.log',
                       help='Log file to monitor (default: traffic.log)')
    parser.add_argument('-k', '--known', default='known_ips.txt',
                       help='File with known IPs (default: known_ips.txt)')
    parser.add_argument('-t', '--tail', action='store_true',
                       help='Continuously monitor log file (like tail -f)')
    
    args = parser.parse_args()
    
    # Create monitor instance
    monitor = SimpleIPMonitor(known_ips_file=args.known)
    
    # Start monitoring
    monitor.monitor_file(args.logfile, tail=args.tail)

if __name__ == "__main__":
    main()