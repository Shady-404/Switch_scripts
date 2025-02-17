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

    # Prompt user for the EtherChannel group number, interfaces to add, interfaces to remove, and mode
    interfaces_to_add = get_user_input("Enter the interface or range of interfaces to add (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2') [Press Enter to skip]: ")
    interfaces_to_remove = get_user_input("Enter the interface or range of interfaces to remove (e.g., 'GigabitEthernet0/3' or 'GigabitEthernet0/3-4') [Press Enter to skip]: ")
    group_no = get_user_input("Enter the EtherChannel group number to modify: ")
    mode = get_user_input("Enter the EtherChannel mode (active, passive, on)")

    # Commands to modify the existing EtherChannel
    commands = []
    if interfaces_to_remove:
        commands.append(f"interface range {interfaces_to_remove}")
        commands.append(f"no channel-group {group_no} mode {mode}")
    if interfaces_to_add:
        commands.append(f"interface range {interfaces_to_add}")
        commands.append(f"channel-group {group_no} mode {mode}")

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device if there are valid commands
    if commands:
        output = net_connect.send_config_set(commands)
        if '% Invalid input detected' in output:
            raise Exception
        elif '% Incomplete command' in output:
            print("Incomplete command. Please check the command syntax and try again.")
        elif '% Ambiguous command' in output:
            print("Ambiguous command. Please provide more specific input.")
        else:
            # Print the output if no errors are found
            print(f"EtherChannel group {group_no} modified. Interfaces added: {interfaces_to_add if interfaces_to_add else 'None'}. Interfaces removed: {interfaces_to_remove if interfaces_to_remove else 'None'}. Mode: {mode if mode else 'Unchanged'}")
    else:
        print("No valid commands to execute. Please provide valid inputs.")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to modify EtherChannel group {group_no}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()