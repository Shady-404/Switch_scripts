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

    # Prompt user for the interface to configure
    interface = get_user_input("Enter the interface to configure (e.g., 'Ethernet0/1' or 'Vlan1'): ")
    dhcp_server_ip = get_user_input("Enter the IP address of the remote DHCP server: ")

    # DHCP relay agent configuration commands
    commands = [
        f'interface {interface}',
        f'ip helper-address {dhcp_server_ip}'
    ]
    
    # If it's not an SVI, add the 'no switchport' command
    if not interface.lower().startswith('vlan'):
        commands.insert(1, 'no switchport')

    # Enter configuration mode
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)
    
    # Define the error messages
    error_messages = [
        '% Invalid input detected',
        '% Incomplete command',
        '% Ambiguous command'
    ]
    
    # Check if any error message is in the output
    if any(error_message in output for error_message in error_messages):
        raise Exception

    # Print the output if no errors are found
    print("Switch configured as a DHCP relay agent successfully")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred while configuring the switch as a DHCP relay agent.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
