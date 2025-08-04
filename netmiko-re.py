from netmiko import ConnectHandler
import re

# R1 connection info
r1 = {
    'device_type': 'cisco_ios',
    'ip': '172.31.48.4',
    'username': 'admin',
    'key_file': '/home/devasc/.ssh/id_rsa.pub',
    'use_keys': True,
}

# R2 connection info  
r2 = {
    'device_type': 'cisco_ios',
    'ip': '172.31.48.5', 
    'username': 'admin',
    'key_file': '/home/devasc/.ssh/id_rsa.pub',
    'use_keys': True,
}

# Function to find active interfaces using regex
def find_active_interfaces(text):
    # Look for lines with "up" status and "up" protocol
    pattern = r'(\S+)\s+(\S+)\s+\S+\s+\S+\s+(up)\s+(up)'
    all_matches = re.findall(pattern, text)
    
    # Separate interfaces with real IPs from unassigned ones
    real_ip_matches = []
    unassigned_matches = []
    
    for interface, ip, status, protocol in all_matches:
        if re.match(r'\d+\.\d+\.\d+\.\d+', ip):  # Real IP address
            real_ip_matches.append((interface, ip, status, protocol))
        else:  # unassigned or other
            unassigned_matches.append((interface, ip, status, protocol))

    return all_matches, real_ip_matches, unassigned_matches

# Function to find uptime using regex
def find_uptime(text):
    # Look for "uptime is" followed by anything
    pattern = r'uptime is (.+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return "Not found"

# Check R1
print("=== Checking R1 ===")
with ConnectHandler(**r1) as ssh:
    # Get uptime
    version = ssh.send_command("show version")
    uptime = find_uptime(version)
    print(f"R1 Uptime: {uptime}")
    
    # Get interfaces
    interfaces = ssh.send_command("show ip interface brief")
    all_active, ip_active, unassigned_active = find_active_interfaces(interfaces)
    
    print(f"R1 Interfaces with IP Addresses:")
    for interface, ip, status, protocol in ip_active:
        print(f"  {interface} - IP: {ip} - Status: {status}/{protocol}")
    
    print(f"R1 Unassigned Active Interfaces:")
    for interface, ip, status, protocol in unassigned_active:
        print(f"  {interface} - {ip} - Status: {status}/{protocol}")

print()

# Check R2
print("=== Checking R2 ===")
with ConnectHandler(**r2) as ssh:
    # Get uptime
    version = ssh.send_command("show version")
    uptime = find_uptime(version)
    print(f"R2 Uptime: {uptime}")
    
    # Get interfaces
    interfaces = ssh.send_command("show ip interface brief")
    all_active, ip_active, unassigned_active = find_active_interfaces(interfaces)
    
    print(f"R2 Interfaces with IP Addresses:")
    for interface, ip, status, protocol in ip_active:
        print(f"  {interface} - IP: {ip} - Status: {status}/{protocol}")
    
    print(f"R2 Unassigned Active Interfaces:")
    for interface, ip, status, protocol in unassigned_active:
        print(f"  {interface} - {ip} - Status: {status}/{protocol}")

print("\nDone!")