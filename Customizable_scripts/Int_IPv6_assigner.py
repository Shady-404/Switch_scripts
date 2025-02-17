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

net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Prompt user for the interface and IPv6 address to assign
    interface = get_user_input("Enter the interface you want to configure (e.g., Ethernet0/0, e0/0, or vlan1): ").lower()
    ipv6_address = get_user_input("Enter the IPv6 address to assign (e.g., 2001:db8::1/64): ")

    # Command to assign IPv6 address to the interface
    if 'vlan' in interface:
        commands = [
            f'interface {interface}',
            f'ipv6 address {ipv6_address}'
        ]
    else:
        commands = [
            f'interface {interface}',
            'no switchport',
            f'ipv6 address {ipv6_address}'
        ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output or "overlaps" in output:
        raise Exception()

    # Print success message
    print(f"IPv6 address {ipv6_address} has been assigned to interface {interface} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to assign IPv6 address to interface {interface}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
