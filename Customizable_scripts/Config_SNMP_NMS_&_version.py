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

    # Prompt user for SNMP host, version, and community string
    snmp_host = get_user_input("Enter the NMS IP address (SNMP host): ")
    snmp_version = get_user_input("Enter the SNMP version (1, 2c, or 3 auth): ")
    snmp_community = get_user_input("Enter the SNMP community string: ")

    # SNMP host configuration command
    command = f'snmp-server host {snmp_host} version {snmp_version} {snmp_community}'

    # Enter configuration mode
    net_connect.config_mode()

    # Send command to the device
    output = net_connect.send_config_set([command])
    
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
    print("SNMP host configured successfully")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred while configuring the SNMP host.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
