from netmiko import ConnectHandler
from jinja2 import Template
import os

# Step 1: Device connection info
device = {
    'device_type': 'cisco_ios',
    'ip': '172.31.48.5',
    'username': 'admin',
    'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
    'use_keys': True,
}

# Step 2: Configuration variables
variables = {
    # OSPF Settings
    'ospf_process': 1,
    'vrf_name': 'control-data',
    'ospf_networks': [
        '172.31.48.0 0.0.0.255',
        '192.168.86.0 0.0.0.255'
    ],
    'area': 0,
    
    # Interface Settings
    'inside_interface': 'g0/0',  # NAT inside only
    'vrf_interfaces': [
        {
            'name': 'g0/1',
            'ip': '172.31.48.7',
            'mask': '255.255.255.240',
            'nat': 'inside',
            'ospf': True
        },
        {
            'name': 'g0/2', 
            'ip': '172.31.48.33',
            'mask': '255.255.255.240',
            'nat': 'inside',
            'ospf': False
        },
        {
            'name': 'g0/3',
            'ip': 'dhcp',
            'mask': None,
            'nat': 'outside',
            'ospf': False
        }
    ],
    
    # Loopback Settings
    'loopback_ip': '1.1.1.2',
    'loopback_mask': '255.255.255.0',
    
    # NAT Settings
    'nat_interface': 'g0/3',
    'nat_acl': 100,
    'nat_network': '172.31.48.0 0.0.0.255',
    
    # Security Settings
    'mgmt_acl': 150,
    'allowed_networks': [
        '172.30.29.0 0.0.0.255',
        '172.31.48.0 0.0.0.255'
    ]
}

# Step 3: Configuration template
template_text = """
router ospf {{ ospf_process }} vrf {{ vrf_name }}
{% for network in ospf_networks %}
 network {{ network }} area {{ area }}
{% endfor %}
 default-information originate always
 exit

interface {{ inside_interface }}
 ip nat inside
 exit

{% for interface in vrf_interfaces %}
interface {{ interface.name }}
 ip vrf forwarding {{ vrf_name }}
{% if interface.ip == 'dhcp' %}
 ip address dhcp
{% else %}
 ip address {{ interface.ip }} {{ interface.mask }}
{% endif %}
 ip nat {{ interface.nat }}
{% if interface.ospf %}
 ip ospf {{ ospf_process }} area {{ area }}
{% endif %}
 no shutdown
 exit

{% endfor %}
interface loopback0
 ip vrf forwarding {{ vrf_name }}
 ip address {{ loopback_ip }} {{ loopback_mask }}
 no shutdown
 ip ospf {{ ospf_process }} area {{ area }}
 exit

ip nat inside source list {{ nat_acl }} interface {{ nat_interface }} vrf {{ vrf_name }} overload

access-list {{ nat_acl }} permit ip {{ nat_network }} any

{% for network in allowed_networks %}
access-list {{ mgmt_acl }} permit tcp {{ network }} any eq telnet
access-list {{ mgmt_acl }} permit tcp {{ network }} any eq 22
{% endfor %}

line vty 0 4
 access-class {{ mgmt_acl }} in
 exit
"""

# Step 4: Fill out the template
template = Template(template_text)
config_commands = template.render(variables)

print("NAT Gateway with OSPF Configuration:")
print("=" * 60)
print(config_commands)
print("=" * 60)

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
    print("✓ NAT Gateway configuration applied!")
    
    # Exit config mode
    connection.exit_config_mode()
    print("✓ Configuration complete!")

print("\nDevice response:")
print(output)