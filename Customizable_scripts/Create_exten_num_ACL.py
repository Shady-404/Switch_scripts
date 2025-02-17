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

    # Prompt user for ACL number
    acl_number = get_user_input("Enter the extended ACL number (100-199 or 2000-2699): ")

    # Prompt user for ACL entries
    acl_entries = []
    print("Enter ACL entries (e.g., 'permit tcp 192.168.1.0 0.0.0.255 any eq 80'). Press 'Enter' to finish!")
    while True:
        entry = get_user_input("Enter an ACL entry: ")
        if entry.strip() == '':
            break
        acl_entries.append(f"access-list {acl_number} {entry}")

    # Enter configuration mode
    net_connect.config_mode()

    # Send ACL configuration commands to the device
    output_acl = net_connect.send_config_set(acl_entries)

    # Prompt user for interface to apply ACL
    interface = get_user_input("Enter the interface to apply the ACL (e.g., 'GigabitEthernet0/1'): ")
    direction = get_user_input("Enter the direction (inbound or outbound) to apply the ACL (in | out): ")

    # Commands to apply the ACL to the specified interface
    apply_acl_commands = [
        f'interface {interface}',
        f'ip access-group {acl_number} {direction}'
    ]

    # Send commands to apply the ACL to the interface
    output_interface = net_connect.send_config_set(apply_acl_commands)

    # Consolidate all outputs
    final_output = output_acl + "\n" + output_interface

    # Check for error messages
    if '% Invalid input detected' in final_output or '% Incomplete command' in final_output or "Access rule can't be configured" in final_output:
        raise Exception("An error occurred during configuration. Please check the ACL entries and interface settings.")

    # Print the success message
    print(final_output)
    print(f"Extended ACL {acl_number} configured and applied to interface {interface} {direction} successfully")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("An error occurred!")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
