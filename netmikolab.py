import os
from netmiko import ConnectHandler

# --- Configuration ---
username = 'admin'
key_file_path = os.path.expanduser('~/.ssh/id_rsa')
devices_ip = [
    "172.31.48.1", 
    "172.31.48.2", 
    "172.31.48.3", 
    "172.31.48.4", 
    "172.31.48.5"
]

# --- Main Script ---
for ip in devices_ip:
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'use_keys': True,
        'key_file': key_file_path
    }
    
    print(f"Connecting to {ip}...")
    
    try:
        net_connect = ConnectHandler(**device)
        print(f"Connected to {ip}. Executing command...")
        
        output = net_connect.send_command("show ip int b")
        print("--- Output ---")
        print(output)
        print("--------------")
        
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")