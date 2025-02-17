from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Please enter the IP address of the switch: ")
username = get_user_input("Please enter your username: ")
password = get_user_input("Please enter your password: ")

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

    # Commands to disable STP
    commands = [
        "configure terminal",
        "no spanning-tree vlan 1-4094",  # Disable STP for all VLANs
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print("Spanning Tree Protocol (STP) has been disabled!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Failed to disable Spanning Tree Protocol (STP).")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

