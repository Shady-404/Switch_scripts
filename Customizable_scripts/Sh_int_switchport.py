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

# Initialize net_connect to None
net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Prompt user for the interface or all interfaces
    interfaces = get_user_input("Please enter the interface (e.g., 'GigabitEthernet0/1') or press Enter for all interfaces: ")

    # Command to show the switchport configuration
    if interfaces.strip() == '':
        command = "show interfaces switchport"
    else:
        command = f"show interfaces {interfaces} switchport"

    # Send command to the device
    output = net_connect.send_command(command)

    # Print the switchport configuration
    print(f"Switchport configuration for {interfaces if interfaces.strip() != '' else 'all interfaces'}:\n{output}")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to retrieve switchport configuration for {interfaces if interfaces.strip() != '' else 'all interfaces'}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
