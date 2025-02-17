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
    acl_number = get_user_input("Enter the standard ACL number (1-99 or 1300-1999): ")

    # Prompt user for remark
    remark = get_user_input("Enter the remark to add: ")

    # Command to add the remark to the ACL
    add_remark_command = f"access-list {acl_number} remark {remark}"

    # Enter configuration mode
    net_connect.config_mode()

    # Send command to add the remark to the ACL
    output = net_connect.send_config_set([add_remark_command])

    # Check for error messages
    if '% Invalid input detected' in output or '% Incomplete command' in output:
        raise Exception("An error occurred while adding the remark. Please check the ACL number and remark and try again.")
    else:
        print(f"Remark '{remark}' added to standard numbered ACL {acl_number} successfully")

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
