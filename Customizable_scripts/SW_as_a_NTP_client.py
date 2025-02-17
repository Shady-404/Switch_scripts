from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt, required=True):
    while True:
        user_input = input(prompt)
        if not required and not user_input:
            return None
        if user_input:
            return user_input
        print("This input is required. Please try again.")

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

    # Collect NTP server configurations
    ntp_servers = []
    while True:
        ntp_server_ip = get_user_input("Enter the IP address of the NTP server (Press Enter to stop): ", required=False)
        if not ntp_server_ip:
            break
        prefer = get_user_input("Prefer this NTP server? (Press Enter to skip): ", required=False)
        if prefer:
            ntp_servers.append(f'ntp server {ntp_server_ip} prefer')
        else:
            ntp_servers.append(f'ntp server {ntp_server_ip}')

    # Send NTP server configuration commands
    if ntp_servers:
        commands = ntp_servers
        output = net_connect.send_config_set(commands)
        
        # Define the error messages
        error_messages = [
            '% Invalid input detected',
            '% Incomplete command',
            '% Ambiguous command',
            'Translating'
        ]
        
        # Check if any error message is in the output
        if any(error_message in output for error_message in error_messages):
            raise Exception

        # Print the output if no errors are found
        print("Switch configured with NTP servers successfully")
        
    else:
        print("No NTP servers were configured.")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred while configuring NTP servers on the switch.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
