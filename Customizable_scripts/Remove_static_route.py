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

    # Prompt user for static route details
    destination_network = get_user_input("Enter the destination network (e.g., 192.168.2.0): ")
    subnet_mask = get_user_input("Enter the subnet mask (e.g., 255.255.255.0): ")
    next_hop_or_interface = get_user_input("Enter the next hop IP address or exit interface (e.g., 192.168.1.1 or GigabitEthernet0/1): ")

    # Command to remove the static route
    command = f"no ip route {destination_network} {subnet_mask} {next_hop_or_interface}"

    # Send command to the device
    net_connect.send_config_set([command])

    # Print success message
    print("Static route removed successfully.")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred!")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
