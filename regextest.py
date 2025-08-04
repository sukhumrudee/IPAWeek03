from netmiko import ConnectHandler
from jinja2 import Template
import os
import re

def regextest(text):
    uptime = r'\S+\s+uptime.+'
    pattern = r'(\S+)\s+(\S+)\s+\S+\s+\S+\s+(up)\s+(up)'
    uptime_match = re.findall(uptime, text)
    all_matches = re.findall(pattern, text)
    print(uptime_match)
    return all_matches

#def finduptime(text):
#    pattern = r'\S+\s+uptime.+'
#    all_matches = re.findall(pattern, text)
#    return all_matches
# Step 1: Device connection info
devices = [
    {
#        'name': 'R1',
        'device_type': 'cisco_ios',
        'ip': '172.31.48.4',
        'username': 'admin',
        'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
        'use_keys': True,
    },
    {
#        'name': 'R2',
        'device_type': 'cisco_ios',
        'ip': '172.31.48.5',
        'username': 'admin',
        'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
        'use_keys': True,
    }
]



# Step 3: Configuration template
template_text = """
do show ip int brief | include up
do show version | include uptime
"""

# Step 4: Fill out the template
template = Template(template_text)
config_commands = template.render()


print(config_commands)

# Step 5: Connect and configure device
for d in devices:

    with ConnectHandler(**d) as connection:
        # Go to enable mode
        connection.enable()
        
        # Send all commands at once
        output = connection.send_config_set(config_commands.strip().split('\n'))
        
        # Exit config mode
        connection.exit_config_mode()

    print("\nDevice response...:")
    for  i in regextest(output):
        print(f"int {i[0]} ip {i[1]} state {i[2]} {i[3]}")

"""
with ConnectHandler(**device2) as connection:
    # Go to enable mode
    connection.enable()
    
    # Send all commands at once
    output = connection.send_config_set(config_commands.strip().split('\n'))
    
    # Exit config mode
    connection.exit_config_mode()

print("\nDevice response of R2:")
for  i in regextest(output):
    print(f"int {i[0]} ip {i[1]} state {i[2]} {i[3]}")
"""