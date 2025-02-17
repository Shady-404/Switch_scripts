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

    # Prompt user for the VLAN ID
    vlan_id = get_user_input("Enter the VLAN ID you want to enable DAI for: ")

    # Command to enable DAI for the specific VLAN
    commands = [
        f'ip arp inspection vlan {vlan_id}'
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception()

    # Print success message
    print(f"Dynamic ARP Inspection has been enabled for VLAN {vlan_id} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to enable Dynamic ARP Inspection for VLAN {vlan_id}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
