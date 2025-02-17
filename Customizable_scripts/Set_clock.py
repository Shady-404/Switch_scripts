from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Enter the IP address of the switch: ")
username = get_user_input("Enter your username: ")
password = get_user_input("Enter your password: ")

# Prompt user for the date and time to set the clock
date_time = get_user_input("Enter the date and time (e.g., 12:30:00 Dec 30 2024): ")

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

    # Command to set the clock
    command = f"clock set {date_time}"

    # Send command to the device
    output = net_connect.send_command_timing(command)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception()

    # Print success message
    print("Clock set successfully.")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"An error occurred")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
