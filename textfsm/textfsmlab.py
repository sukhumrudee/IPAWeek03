from netmiko import ConnectHandler
import os

os.environ['NET_TEXTFSM'] = os.path.dirname(os.path.abspath(__file__))

devices = [
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.48.4',
        'username': 'admin',
        'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
        'use_keys': True,
    },
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.48.5',
        'username': 'admin',
        'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
        'use_keys': True,
    },
    {
        'device_type': 'cisco_ios',
        'ip': '172.31.48.3',
        'username': 'admin',
        'key_file': os.path.expanduser("~/.ssh/id_rsa.pub"),
        'use_keys': True,
    }
]

for d in devices:
    with ConnectHandler(**d) as connection:
        output = connection.send_command('sh cdp neighbors', use_textfsm=True)
        connection.exit_config_mode()
    for one in output:
        print(f"{one['neighbor_name']} is connected to your {one['local_interface']}")