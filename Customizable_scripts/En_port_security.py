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

    # Prompt user for the interface or range of interfaces
    interfaces = get_user_input("Enter the interface or range of interfaces (e.g., 'GigabitEthernet0/1' or 'GigabitEthernet0/1-2'): ")
    max_mac_addresses = get_user_input("Enter the maximum number of MAC addresses allowed [default: 1]: ")
    violation_mode = get_user_input("Enter the violation mode (protect, restrict, or shutdown) [default: shutdown]: ")

    # Set default values if user presses Enter
    if not max_mac_addresses:
        max_mac_addresses = "1"
    if not violation_mode:
        violation_mode = "shutdown"

    # Prompt user for the MAC addresses to be allowed
    mac_addresses = []
    while True:
        mac_address = get_user_input("Enter a MAC address to be allowed (or press Enter to finish): ")
        if mac_address:
            mac_addresses.append(mac_address)
        else:
            break

    # Commands to enable port security on the specified interface(s) and specify the MAC addresses
    commands = [
        "configure terminal",
        f"interface range {interfaces}",
        "switchport port-security",
        f"switchport port-security maximum {max_mac_addresses}",
        f"switchport port-security violation {violation_mode}",
    ]
    for mac in mac_addresses:
        commands.append(f"switchport port-security mac-address {mac}")
    commands.append("end")

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for dynamic port error
    if "Command rejected" in output and "is a dynamic port" in output:
        print("One or more interfaces are dynamic ports. Port security cannot be enabled on dynamic ports!")
    elif "Found duplicate mac-address" in output: 
        print("Duplicate MAC address found. Port security cannot be enabled with duplicate MAC addresses!")
    else:
        # Print success message
        print(f"Port security has been enabled on interface(s) {interfaces} with a maximum of {max_mac_addresses} MAC addresses and violation mode set to {violation_mode} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to enable port security on interface(s) {interfaces}.")


finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
