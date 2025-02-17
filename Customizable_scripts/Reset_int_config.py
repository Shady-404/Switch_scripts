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

    # Prompt user for the interface or range of interfaces
    interfaces = get_user_input("Enter the interface or range of interfaces (e.g., Ethernet0/0, e0/0, or a range like e0/0-3): ")

    # Commands to reset the specified interface(s) to default configuration
    commands = [
        "configure terminal",
        f"default interface range {interfaces}",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"Interface(s) {interfaces} has/have been reset to their default configuration successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to reset interface(s) {interfaces} to default configuration.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
