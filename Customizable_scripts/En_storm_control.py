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

    # Prompt user for interface and storm control parameters
    interface = get_user_input("Enter the interface (e.g., GigabitEthernet0/1): ")
    traffic_type = get_user_input("Enter the traffic type to enable (broadcast, multicast, or unicast): ")
    suppression_level = get_user_input("Enter the suppression level percentage (1-100): ")

    # Commands to enable storm control on the specified interface
    commands = [
        f'interface {interface}',
        f'storm-control {traffic_type} level {suppression_level}',
        'exit'
    ]

    # Enter configuration mode
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception()

    # Print success message
    print(f"Storm control for {traffic_type} traffic set to {suppression_level}% on interface {interface} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to configure storm control for {traffic_type} traffic on interface {interface}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
