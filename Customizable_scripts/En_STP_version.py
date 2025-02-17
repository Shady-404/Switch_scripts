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

    # Prompt user for the STP version to enable
    print("Select the STP version to enable:")
    print("1. PVST+ (Per-VLAN Spanning Tree Plus)")
    print("2. Rapid PVST+ (Rapid Per-VLAN Spanning Tree Plus)")
    print("3. MST (Multiple Spanning Tree)")
    stp_version = get_user_input("Enter the number corresponding to the STP version: ")

    # Determine the command based on user selection
    if stp_version == "1":
        stp_command = "spanning-tree mode pvst"
    elif stp_version == "2":
        stp_command = "spanning-tree mode rapid-pvst"
    elif stp_version == "3":
        stp_command = "spanning-tree mode mst"
    else:
        print("Invalid selection. Please run the script again and select a valid option.")
        net_connect.disconnect()
        exit()

    # Commands to enable the selected STP version
    commands = [
        "configure terminal",
        stp_command,
        "end"
    ]

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Print success message
    print(f"Spanning Tree Protocol (STP) has been enabled with {stp_command}!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Failed to enable Spanning Tree Protocol (STP).")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

