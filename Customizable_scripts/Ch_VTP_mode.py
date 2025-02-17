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

    # Enter configuration mode
    net_connect.config_mode()

    # Prompt user for the desired VTP mode
    vtp_mode = get_user_input("Enter the VTP mode (server/client/transparent): ").lower()

    # Commands to change the VTP mode
    commands = [
        f"vtp mode {vtp_mode}",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"VTP mode has been changed to {vtp_mode} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Failed to change VTP mode.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
