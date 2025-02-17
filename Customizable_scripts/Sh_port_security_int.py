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

net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Prompt user for the specific interface
    interface = get_user_input("Enter the interface (e.g., 'GigabitEthernet0/1'): ")

    # Command to show port security configuration for the specific interface
    command = f"show port-security interface {interface}"

    # Send command to the device
    output = net_connect.send_command(command)

    # Print the output
    print(f"Port Security Configuration for {interface}:\n")
    print(output)

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to retrieve port security configuration for {interface}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

