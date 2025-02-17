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

    # Enter enable mode
    net_connect.enable()

    # Prompt user for timestamp options
    timestamp_option = get_user_input("Enter the timestamp option (e.g., 'datetime', 'uptime'): ")

    # Commands to configure service timestamps log
    commands = [
        f'service timestamps log {timestamp_option}'
    ]

    # Enter configuration mode
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print a success message
    print(f"Service timestamps log configured successfully with option {timestamp_option}")

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
