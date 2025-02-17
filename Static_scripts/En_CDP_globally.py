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

    # Command to enable CDP globally
    commands = [
        "configure terminal",
        "cdp run",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print("CDP has been enabled globally!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Failed to enable CDP globally.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

