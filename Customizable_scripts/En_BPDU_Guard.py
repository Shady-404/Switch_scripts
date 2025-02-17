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

    # Prompt user for the interface or range of interfaces to configure
    interfaces = get_user_input("Please enter the interface or range of interfaces to enable BPDU Guard (e.g., GigabitEthernet0/1 or GigabitEthernet0/1-2): ")

    # Commands to enable BPDU Guard on the specified interface(s)
    commands = [
        "configure terminal",
        f"interface range {interfaces}",
        "spanning-tree bpduguard enable",
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"BPDU Guard has been enabled on {interfaces}!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to enable BPDU Guard on {interfaces}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

