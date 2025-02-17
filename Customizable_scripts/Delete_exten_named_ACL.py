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

    # Prompt user for ACL name
    acl_name = get_user_input("Enter the extended ACL name to delete: ")

    # Command to delete the entire ACL
    delete_acl_command = f"no ip access-list extended {acl_name}"

    # Enter configuration mode
    net_connect.config_mode()

    # Send the command to delete the ACL
    output = net_connect.send_config_set([delete_acl_command])

    # Check for error messages
    if '% Invalid input detected' in output or '% Incomplete command' in output:
        raise Exception("An error occurred while deleting the ACL. Please check the ACL name and try again.")
    else:
        # Print the output and success message
        print(output)
        print(f"Extended named ACL '{acl_name}' deleted successfully")

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
