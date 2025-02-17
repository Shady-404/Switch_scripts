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
    methods = get_user_input("Enter the authentication methods (e.g., local, group radius, group tacacs+): ")

    # Prompt for the number of users to add
    num_users = int(get_user_input("Enter the number of users to add: "))

    # Collect user details
    user_commands = []
    for i in range(num_users):
        username = get_user_input(f"Enter username for user {i+1}: ")
        password = get_user_input(f"Enter password for user {i+1}: ")
        privilege = get_user_input(f"Enter privilege level for user {i+1} (0-15): ")
        user_commands.append(f'username {username} privilege {privilege} secret {password}')

    # Commands to create a named authentication list, add users and set privilege levels
    commands = [
        'aaa new-model',
        f'aaa authentication login {auth_list_name} {methods}'
    ] + user_commands

    # Enter configuration mode and send commands
    net_connect.config_mode()
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception("An error occurred while creating the named authentication list. Please check the input methods.")

    # Print success message
    print(f"Named authentication list '{auth_list_name}' configured successfully with methods: ", methods)
    print(output)

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
