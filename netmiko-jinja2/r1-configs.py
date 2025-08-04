from netmiko import ConnectHandler
from jinja2 import Template
import os

# Step 1: Device connection info
device = {
    'device_type': 'cisco_ios',
    'ip': '172.31.48.4',
    'username': 'admin',
    'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
    'use_keys': True,
}

# Step 2: Configuration variables
variables = {
    'ospf_process': 1,
    'vrf_name': 'control-data',
    'ospf_network': '172.31.48.0 0.0.0.255',
    'area': 0,
    'interface': 'g0/2',
    'interface_ip': '172.31.148.6',
    'interface_mask': '255.255.255.240',
    'loopback_ip': '1.1.1.1',
    'loopback_mask': '255.255.255.0',
    'acl_number': 150,
    'allowed_networks': [
        '172.30.29.0 0.0.0.255',
        '172.31.48.0 0.0.0.255'
    ]
}

# Step 3: Configuration template
template_text = """
router ospf {{ ospf_process }} vrf {{ vrf_name }}
 network {{ ospf_network }} area {{ area }}
 exit

interface {{ interface }}
 ip vrf forwarding {{ vrf_name }}
 ip address {{ interface_ip }} {{ interface_mask }}
 ip ospf {{ ospf_process }} area {{ area }}
 no shutdown
 exit

interface loopback0
 ip vrf forwarding {{ vrf_name }}
 ip address {{ loopback_ip }} {{ loopback_mask }}
 no shutdown
 ip ospf {{ ospf_process }} area {{ area }}
 exit

{% for network in allowed_networks %}
access-list {{ acl_number }} permit tcp {{ network }} any eq telnet
access-list {{ acl_number }} permit tcp {{ network }} any eq 22
{% endfor %}

line vty 0 4
 access-class {{ acl_number }} in
 exit
"""

# Step 4: Fill out the template
template = Template(template_text)
config_commands = template.render(variables)

print("OSPF VRF Configuration to be applied:")
print("=" * 50)
print(config_commands)
print("=" * 50)

# Step 5: Connect and configure device
with ConnectHandler(**device) as connection:
    # Go to enable mode
    connection.enable()
    print("✓ Entered enable mode")
    
    # Go to config mode
    connection.config_mode()
    print("✓ Entered config mode")
    
    # Send all commands at once
    output = connection.send_config_set(config_commands.strip().split('\n'))
    print("✓ OSPF VRF configuration applied!")
    
    # Exit config mode
    connection.exit_config_mode()
    print("✓ Configuration complete!")

print("\nDevice response:")
print(output)