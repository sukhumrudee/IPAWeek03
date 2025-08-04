from netmiko import ConnectHandler
import os

device_ip = "172.31.144.3"
username = "admin"
key_path = os.path.expanduser("~/.ssh/id_rsa.pub")

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'key_file' : key_path,
    'use_keys': True,
}
with ConnectHandler(**device_params) as ssh:
    result = ssh.enable()
    print(result)
    result = ssh.config_mode()
    print(result)
    result = ssh.send_command_timing("vlan 101")
    print(result)
    result = ssh.send_command_timing("name control-data")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)
    result = ssh.send_command_timing("int vlan 101")
    print(result)
    result = ssh.send_command_timing("no shut")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)
    result = ssh.send_command_timing("int range g0/1, g1/1")
    print(result)
    result = ssh.send_command_timing("switch mode access")
    print(result)
    result = ssh.send_command_timing("switch access vlan 101")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    result = ssh.send_command_timing("access-list 150 permit tcp 172.30.29.0 0.0.0.255 any eq telnet")
    print(result)
    result = ssh.send_command_timing("access-list 150 permit tcp 172.30.29.0 0.0.0.255 any eq 22")
    print(result)
    result = ssh.send_command_timing("access-list 150 permit tcp 172.31.144.0 0.0.0.255 any eq telnet")
    print(result)
    result = ssh.send_command_timing("access-list 150 permit tcp 172.31.144.0 0.0.0.255 any eq 22")
    print(result)
    result = ssh.send_command_timing("line vty 0 4")
    print(result)
    result = ssh.send_command_timing("access-class 150 in")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    ssh.disconnect()