from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Enter the IP address of the switch: ")
username = get_user_input("Enter your username: ")
password = get_user_input("Enter your password: ")

# Define the device details
device = {
    'device_type': 'cisco_ios',
    'host': switch_ip,
    'username': username,
    'password': password,
}

# Initialize net_connect to None
net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Prompt user for DHCP pool details
    pool_name = get_user_input("Enter the DHCP pool name: ")
    network = get_user_input("Enter the network (e.g., '192.168.1.0'): ")
    subnet_mask_or_prefix_len = get_user_input("Enter the subnet mask or prefix length (e.g., '255.255.255.0' or /24): ")
    default_router = get_user_input("Enter the default gateway IP address: ")
    dns_server = get_user_input("Enter the DNS server IP addresses (e.g., '8.8.8.8'): ")
    domain_name = get_user_input("Enter the domain name: ")
    lease_days = get_user_input("Enter the lease time in days: ")
    lease_hours = get_user_input("Enter the lease time in hours: ")
    lease_minutes = get_user_input("Enter the lease time in minutes: ")
    excluded_addresses = get_user_input("Enter the range of excluded addresses (e.g., '192.168.1.1 192.168.1.10'): ")

    # DHCP configuration commands
    commands = [
        f'ip dhcp excluded-address {excluded_addresses}',
        f'ip dhcp pool {pool_name}',
        f'network {network} {subnet_mask_or_prefix_len}',
        f'default-router {default_router}',
        f'dns-server {dns_server}',
        f'domain-name {domain_name}',
        f'lease {lease_days} {lease_hours} {lease_minutes}',
    ]

    # Enter configuration mode
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)
    
    # Define the error messages
    error_messages = [
        '% Invalid input detected',
        '% Incomplete command',
        '% Ambiguous command',
        'invalid network',
        '% A pool already exists'
    ]
    
    # Check if any error message is in the output
    if any(error_message in output for error_message in error_messages):
            raise Exception

    # Print the output if no errors are found
    print("DHCP server configured successfully")
except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred while configuring the DHCP server.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
