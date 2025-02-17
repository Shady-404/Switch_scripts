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

    # Prompt user for ACL name or number
    acl_identifier = get_user_input("Enter the ACL name or number: ")

    # Prompt user for starting sequence number and increment
    start_seq = get_user_input("Enter the starting sequence number: ")
    increment = get_user_input("Enter the increment value: ")

    # Command to resequence the ACL
    resequence_acl_command = f"ip access-list resequence {acl_identifier} {start_seq} {increment}"

    # Enter configuration mode
    net_connect.config_mode()

    # Send the command to resequence the ACL
    output = net_connect.send_config_set([resequence_acl_command])

    # Check for error messages
    if '% Invalid input detected' in output or '% Incomplete command' in output:
        raise Exception("An error occurred while resequencing the ACL. Please check the ACL identifier and try again.")
    else:
        print(f"ACL {acl_identifier} resequenced successfully with starting sequence {start_seq} and increment {increment}")

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
