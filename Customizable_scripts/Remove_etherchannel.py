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

    # Prompt user for the EtherChannel group number and interfaces
    interfaces = get_user_input("Enter the interface or range of interfaces (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2'): ")
    group_no = get_user_input("Enter the EtherChannel group number to remove: ")
    mode = get_user_input("Enter the EtherChannel mode (active, passive, on): ")

    # Commands to remove EtherChannel
    commands = [
        f"interface range {interfaces}",
        f"no channel-group {group_no} mode {mode}",
        "exit",
        f"no interface port-channel {group_no}",
        "exit"
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for common errors in the output
    if '% Invalid input detected' in output:
        raise Exception
    elif '% Incomplete command' in output:
        print("Incomplete command. Please check the command syntax and try again.")
    elif '% Ambiguous command' in output:
        print("Ambiguous command. Please provide more specific input.")
    else:
        print(f"EtherChannel group {group_no} removed from interfaces {interfaces}.")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to remove EtherChannel group {group_no}")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()