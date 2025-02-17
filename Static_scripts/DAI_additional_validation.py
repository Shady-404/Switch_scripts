from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt, default=None):
    user_input = input(prompt)
    return user_input if user_input else default

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

    # Prompt user for the validation type
    validation_type = get_user_input("Enter the validation type (src-mac, dst-mac, ip, or all): ")

    # Adjust validation type if 'all' is selected
    if validation_type == "all":
        validation_type = "src-mac dst-mac ip"

    # Command to configure IP ARP inspection validation
    commands = [
        f'ip arp inspection validate {validation_type}'
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception()

    # Print success message
    print(f"IP ARP Inspection validation has been set to {validation_type} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to configure IP ARP Inspection validation.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
