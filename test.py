# quick_test.py
import subprocess


# # Create test files
# with open('known_ips.txt', 'w') as f:
#     f.write("192.168.1.0/24\n8.8.8.8\n")

# with open('traffic.log', 'w') as f:
#     f.write("SRC=192.168.1.100 DST=8.8.8.8\n")
#     f.write("SRC=192.168.1.101 DST=1.2.3.4\n")  # Unknown!

# Run monitor
print("Testing MVP monitor...")
subprocess.run(['python3', '/home/mandillahjr/Documents/Code/Projects/Logistrar/ip-monitor-mvp/monitor.py', '-f', '/home/mandillahjr/Documents/Code/Projects/Logistrar/ip-monitor-mvp/traffic.log'])