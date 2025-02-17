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
    acl_name = get_user_input("Enter the standard ACL name: ")

    # Prompt user for remark
    remark = get_user_input("Enter the remark to add: ")

    # Commands to enter ACL configuration mode and add the remark
    commands = [
        f"ip access-list standard {acl_name}",
        f"remark {remark}"
    ]

    # Enter configuration mode
    net_connect.config_mode()

    # Send commands to add the remark to the ACL
    output = net_connect.send_config_set(commands)

    # Check for error messages
    if '% Invalid input detected' in output or '% Incomplete command' in output:
        raise Exception("An error occurred while adding the remark. Please check the ACL name and remark and try again.")
    else:
        print(f"Remark '{remark}' added to standard named ACL '{acl_name}' successfully")

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
