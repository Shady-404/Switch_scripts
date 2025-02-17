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

    # Prompt user for the RADIUS server hostname or IP address and server group
    radius_server = get_user_input("Enter the RADIUS server hostname or IP address: ")
    server_group = get_user_input("Enter the server group the server belongs to: ")

    # Command to show the AAA dead-criteria for the RADIUS server
    command = f"show aaa dead-criteria radius {radius_server} line {server_group}"

    # Send command to the device
    output = net_connect.send_command(command)

    # Check for invalid input error
    if "Invalid input detected" or "Incomplete command" in output:
        raise Exception()

    # Print the output
    print(f"AAA Dead-Criteria RADIUS {radius_server} Line {server_group}:\n{output}")

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
