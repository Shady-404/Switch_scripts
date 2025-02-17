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

    # Prompt user for the timezone details
    timezone_name = get_user_input("Enter the timezone name (e.g., 'PST', 'EST'): ")
    timezone_offset_hours = get_user_input("Enter the timezone offset in hours (e.g., '-8', '+5'): ")
    timezone_offset_minutes = get_user_input("Enter the timezone offset in minutes (e.g., '0', '30'): ")

    # Clock timezone configuration command
    commands = [
        f'clock timezone {timezone_name} {timezone_offset_hours} {timezone_offset_minutes}'
    ]

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
    print("Switch clock timezone configured successfully")
    print(output)

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred while configuring the clock timezone on the switch.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
