from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Enter the IP address of the switch: ")
username = get_user_input("Enter your current username: ")
password = get_user_input("Enter your current password: ")

# Prompt user for new SSH username and password
new_username = get_user_input("Enter the new SSH username: ")
new_password = get_user_input("Enter the new SSH password: ")

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

    # Commands to remove old usernames and add the new SSH username and password
    commands = [
        f"username {new_username} privilege 15 secret {new_password}",
        f"no username {username} privilege 15 secret {password}",
        f"wr"

    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"SSH username and password changed successfully to {new_username}.")

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