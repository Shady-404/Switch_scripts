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

    # Prompt for authentication methods
    methods = get_user_input("Enter the authentication methods (e.g., local, group radius, group tacacs+): ")

    # Commands to configure the default authentication list with specified methods
    commands = [
        'aaa new-model',
        f'aaa authentication login default {methods}'
    ]

    # Enter configuration mode and send commands
    net_connect.config_mode()
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception("An error occurred while configuring the default authentication list. Please check the input methods.")

    # Print success message
    print("Default authentication list configured successfully with methods: ", methods)

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
