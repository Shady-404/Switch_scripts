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

    # Prompt for the interface and new MAC address
    interface = get_user_input("Enter the interface to configure (e.g., Ethernet0/0, e0/0): ").lower()
    new_mac_address = get_user_input("Enter the new MAC address (e.g., 001A.2B3C.4D5E): ")

    # Commands to change the MAC address
    commands = [
        f'interface {interface}',
        f'mac-address {new_mac_address}',
        'exit'
    ]

    # Enter configuration mode and send commands
    net_connect.config_mode()
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output or "% Malformed hex mac address" in output:
        raise Exception("An error occurred while changing the MAC address! Please check the interface and MAC address format.")

    # Print success message
    print(f"MAC address {new_mac_address} has been assigned to interface {interface} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"An error occurred!")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
