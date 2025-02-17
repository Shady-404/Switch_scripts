from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

# Prompt user for credentials and switch IP address
switch_ip = get_user_input("Please enter the IP address of the switch: ")
username = get_user_input("Please enter your username: ")
password = get_user_input("Please enter your password: ")

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

    # Prompt user for the interface or range of interfaces, VLANs, and encapsulation method
    interfaces = get_user_input("Please enter the interface or range of interfaces (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2'): ")
    vlans = get_user_input("Please enter the VLANs to allow (e.g., '10,20,30'): ")
    encapsulation = get_user_input("Please enter the encapsulation method (isl or dot1q): ").strip().lower()

    # Commands to enable the trunk port with specific VLANs and encapsulation method
    commands = [
        "configure terminal",
        f"interface range {interfaces}",
        f"switchport trunk encapsulation {encapsulation}",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlans}",
        "no shutdown",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for common errors
    if 'Command rejected' in output:
        print(f"Failed to enable trunk port(s) {interfaces}.")
    else:
        # Print success message
        print(f"Trunk port(s) {interfaces} has/have been enabled with VLANs {vlans} and encapsulation {encapsulation}!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to enable trunk port(s) {interfaces}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

