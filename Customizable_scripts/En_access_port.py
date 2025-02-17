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

    # Prompt user for the VLAN ID and interface or range of interfaces
    vlan_id = get_user_input("Enter the VLAN ID: ")
    interfaces = get_user_input("Enter the interface or range of interfaces (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2'): ")

    # Commands to enable the access port with VLAN ID
    commands = [
        "configure terminal",
        f"interface range {interfaces}",
        f"switchport access vlan {vlan_id}",
        "switchport mode access",
        "no shutdown",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for failure message
    if 'Command rejected' in output:
        print(f"Failed to enable access port(s) {interfaces}.")
    else:
        # Print success message
        print(f"Access port(s) {interfaces} has/have been enabled on VLAN {vlan_id}!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to enable access port(s) {interfaces}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
