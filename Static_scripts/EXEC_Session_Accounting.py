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

    # Commands to configure EXEC session accounting
    commands = [
        'aaa new-model',
        'aaa accounting exec default start-stop local'
    ]

    # Enter configuration mode and send commands
    net_connect.config_mode()
    output = net_connect.send_config_set(commands)

    # Print success message
    print("EXEC session accounting configured successfully!")

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
