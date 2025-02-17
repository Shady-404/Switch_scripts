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
    vlan_id = get_user_input("Enter the VLAN ID you want to verify DAI configuration for: ")

    # Command to verify DAI configuration for the specific VLAN
    command = f"show ip arp inspection vlan {vlan_id}"

    # Send command to the device and capture the output
    output = net_connect.send_command(command)

    # Print the DAI configuration for the specific VLAN
    print(f"Dynamic ARP Inspection Configuration for VLAN {vlan_id}:")
    print(output)

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"An error occurred")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
