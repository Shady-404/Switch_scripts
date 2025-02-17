from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Enter the IP address of the switch: ")
username = get_user_input("Enter your username: ")
password = get_user_input("Enter your password: ")

# Prompt user for TFTP server details
tftp_server = get_user_input("Enter the TFTP server address or name: ")
file_name = get_user_input("Enter the name of the saved file: ")

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

    # Command to save the running configuration to TFTP server
    command = f"copy running-config tftp://{tftp_server}/{file_name}"

    # Send command to the device
    net_connect.send_command_timing(command)
    net_connect.send_command_timing("\n")  # Confirm the command

    # Print success message
    print(f"Configuration saved to TFTP server successfully as {file_name}.")

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
