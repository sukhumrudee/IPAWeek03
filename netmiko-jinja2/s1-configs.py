from netmiko import ConnectHandler
from jinja2 import Template
import os

# Step 1: Device connection info
device = {
    'device_type': 'cisco_ios',
    'ip': '172.31.48.3',
    'username': 'admin',
    'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
    'use_keys': True,
}

# Step 2: Configuration variables (the values we want to change)
variables = {
    'vlan_id': 101,
    'vlan_name': 'control-data',
    'interfaces': 'g0/1, g1/1',
    'acl_number': 150,
    'networks': [
        '172.30.29.0 0.0.0.255',
        '172.31.48.0 0.0.0.255'
    ]
}

# Step 3: Configuration template (like a form to fill out)
template_text = """
vlan {{ vlan_id }}
 name {{ vlan_name }}
 exit

interface vlan {{ vlan_id }}
 no shutdown
 exit

interface range {{ interfaces }}
 switchport mode access
 switchport access vlan {{ vlan_id }}
 exit

{% for network in networks %}
access-list {{ acl_number }} permit tcp {{ network }} any eq telnet
access-list {{ acl_number }} permit tcp {{ network }} any eq 22
{% endfor %}

line vty 0 4
 access-class {{ acl_number }} in
 exit
"""

# Step 4: Fill out the template with our variables
template = Template(template_text)
config_commands = template.render(variables)

print("Here's what will be sent to the device:")
print("=" * 40)
print(config_commands)
print("=" * 40)

# Step 5: Connect to device and send the configuration
with ConnectHandler(**device) as connection:
    # Go to enable mode
    connection.enable()
    print("✓ Entered enable mode")
    
    # Go to config mode
    connection.config_mode()
    print("✓ Entered config mode")
    
    # Send all the commands at once
    output = connection.send_config_set(config_commands.strip().split('\n'))
    print("✓ Configuration sent!")
    
    # Exit config mode
    connection.exit_config_mode()
    print("✓ Done!")

print("\nDevice response:")
print(output)