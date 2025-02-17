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

    # Prompt user for the VLAN IDs to delete (comma-separated)
    vlan_ids = get_user_input("Enter the VLAN IDs to delete (comma-separated): ").split(',')

    # Iterate through each VLAN ID and delete it
    for vlan_id in vlan_ids:
        vlan_id = vlan_id.strip()  # Remove any leading/trailing whitespace
        commands = [
            "configure terminal",
            f"no vlan {vlan_id}",
            "end"
        ]
        output = net_connect.send_config_set(commands)
        print(f"VLAN(s) {vlan_id} has/have been deleted successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to delete VLANs.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
