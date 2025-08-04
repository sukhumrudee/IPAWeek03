from netmiko import ConnectHandler
import os

device_ip = "172.31.48.5"
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
    result = ssh.send_command_timing("router ospf 1 vrf control-data")
    print(result)
    result = ssh.send_command_timing("network 172.31.144.0 0.0.0.255 area 0")
    print(result)
    result = ssh.send_command_timing("network 192.168.122.0 0.0.0.255 area 0")
    print(result)
    result = ssh.send_command_timing("default-information originate always")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)
    result = ssh.send_command_timing("int g0/0")
    print(result)
    result = ssh.send_command_timing("ip nat inside")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)
    result = ssh.send_command_timing("int g0/1")
    print(result)
    result = ssh.send_command_timing("ip vrf forwarding control-data")
    print(result)
    result = ssh.send_command_timing("ip add 172.31.144.7 255.255.255.240")
    print(result)
    result = ssh.send_command_timing("ip nat inside")
    print(result)
    result = ssh.send_command_timing("no shut")
    print(result)
    result = ssh.send_command_timing("ip ospf 1 area 0")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    result = ssh.send_command_timing("int g0/2")
    print(result)
    result = ssh.send_command_timing("ip vrf forwarding control-data")
    print(result)
    result = ssh.send_command_timing("ip address 172.31.144.33 255.255.255.240")
    print(result)
    result = ssh.send_command_timing("ip nat inside")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    result = ssh.send_command_timing("int g0/3")
    print(result)
    result = ssh.send_command_timing("ip vrf forwarding control-data")
    print(result)
    result = ssh.send_command_timing("ip address dhcp")
    print(result)
    result = ssh.send_command_timing("ip nat outside")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    result = ssh.send_command_timing("int loopback0")
    print(result)
    result = ssh.send_command_timing("ip vrf forwarding control-data")
    print(result)
    result = ssh.send_command_timing("ip add 1.1.1.2 255.255.255.0")
    print(result)
    result = ssh.send_command_timing("no shut")
    print(result)
    result = ssh.send_command_timing("ip ospf 1 area 0")
    print(result)
    result = ssh.send_command_timing("exit")
    print(result)

    result = ssh.send_command_timing("ip nat inside source list 100 interface g0/3 vrf control-data overload")
    print(result)
    result = ssh.send_command_timing("access-list 100 permit ip 172.31.144.0 0.0.0.255 any")
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