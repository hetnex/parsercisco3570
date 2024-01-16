import re

# Define regex patterns for various configuration elements
interface_regex = r"interface (\S+)"
vlan_regex = r"vlan (\d+)"
ip_address_regex = r"ip address (\S+) (\S+)"
portfast_regex = r"switchport mode access\s+spanning-tree portfast"
shutdown_regex = r"shutdown"
hostname_regex = r"hostname (\S+)"
default_gateway_regex = r"ip default-gateway (\S+)"
snmp_community_regex = r"snmp-server community (\S+) ro (\S+)"
snmp_host_regex = r"snmp-server host (\S+) (\S+)"
ntp_server_regex = r"ntp server (\S+)"

# Read the Cisco Switch configuration
with open('Config-Switch-3750.txt', 'r') as f:
    configuration = f.read()

# Extract information from the configuration
switch_name = re.findall(hostname_regex, configuration)[0]

# Extract VLAN information
vlans = []
for line in configuration.splitlines():
    if re.match(vlan_regex, line):
      vlans.append(int(re.match(vlan_regex, line).group(1)))

# Extract IP addresses and interfaces
interfaces = {}
for line in configuration.splitlines():
    if re.match(interface_regex, line):
        match = re.match(interface_regex, line)
        if match:
            interface_name = match.group(1)

        if re.search(ip_address_regex, line):
            ip_address, mask = re.findall(ip_address_regex, line)[0]
            interfaces[interface_name] = {'ip_address': ip_address, 'mask': mask}

        if re.search(portfast_regex, line):
            interfaces[interface_name]['portfast'] = True

        if re.search(shutdown_regex, line):
            interfaces[interface_name]['shutdown'] = True

# Extract other configuration information
default_gateway = re.findall(default_gateway_regex, configuration)[0]
snmp_communities = []
for line in configuration.splitlines():
    if re.match(snmp_community_regex, line):
      match = re.match(snmp_community_regex, line)
      if match:
          snmp_communities.append([match.group(1), match.group(2)])
snmp_hosts = []
for line in configuration.splitlines():
    if re.match(snmp_host_regex, line):
      match = re.match(snmp_host_regex, line)
      if match:
          ip_address, community = match.group(1), match.group(2)
          snmp_hosts.append([ip_address, community])
ntp_servers = []
for line in configuration.splitlines():
    if re.match(ntp_server_regex, line):
      match = re.match(ntp_server_regex, line)
      if match:
          ip_address = match.group(1)
          ntp_servers.append(ip_address)

# Print the extracted information
print(f"Switch name: {switch_name}")
print(f"VLANs: {vlans}")
print(f"Interfaces:")
for interface_name, interface_config in interfaces.items():
    print(f"    Name: {interface_name}")
    print(f"    IP address: {interface_config.get('ip_address')}")
    print(f"    Mask: {interface_config.get('mask')}")
    print(f"    Portfast: {interface_config.get('portfast', False)}")
    print(f"    Shutdown: {interface_config.get('shutdown', False)}")

print(f"Default gateway: {default_gateway}")
print(f"SNMP communities: {snmp_communities}")
print(f"SNMP hosts: {snmp_hosts}")
print(f"NTP servers: {ntp_servers}")
