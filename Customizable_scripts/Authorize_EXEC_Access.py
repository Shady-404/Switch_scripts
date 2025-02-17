from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Enter the IP address of the switch: ")
admin_username = get_user_input("Enter the admin username: ")
admin_password = get_user_input("Enter the admin password: ")

# Define the device details
device = {
    'device_type': 'cisco_ios',
    'host': switch_ip,
    'username': admin_username,
    'password': admin_password,
}

net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Prompt for the named authentication list and methods
    auth_list_name = get_user_input("Enter the name for the authentication list: ")
    methods = get_user_input("Enter the authentication methods (e.g., local): ")

    # Commands to configure authorization for EXEC access
    commands = [
        'aaa new-model',
        f'aaa authentication login {auth_list_name} {methods}',
        f'aaa authorization exec {auth_list_name} local'
    ]

    # Enter configuration mode and send commands
    net_connect.config_mode()
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"Authorization for EXEC access configured successfully with methods: ", methods)

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
