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

    # Prompt user for the desired VTP version
    vtp_version = get_user_input("Enter the VTP version (1/2/3): ")

    # Commands to change the VTP version
    commands = [
        f"vtp version {vtp_version}",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Cannot set the version" in output:
        raise Exception("Cannot set the version. Please ensure the VTP domain name is configured.")

    # Print success message
    print(f"VTP version has been changed to version {vtp_version} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to change VTP version.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()