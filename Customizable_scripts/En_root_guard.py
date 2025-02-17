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

    # Prompt user for interface or range of interfaces
    interfaces = get_user_input("Enter the interface or range of interfaces (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2'): ")

    # Commands to enable Root Guard
    commands = [
        f"interface range {interfaces}",
        "spanning-tree guard root",
        "exit"
    ]

    # Send commands to the device
    net_connect.send_config_set(commands)

    # Print success message
    print(f"Root Guard enabled on {interfaces} successfully.")

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
