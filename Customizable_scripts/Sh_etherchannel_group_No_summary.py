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

# Initialize net_connect to None
net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    while True:
        # Prompt user for the EtherChannel group number
        group_no = get_user_input("Enter the EtherChannel group number: ")

        # Command to show EtherChannel information for the specified group
        command = f"show etherchannel {group_no} summary"

        # Send command to the device
        output = net_connect.send_command(command)

        # Check for invalid input message in the output
        if '% Invalid input detected' in output:
            print(f"Invalid EtherChannel group number: {group_no}. Please try again.")
        else:
            # Print the EtherChannel information if the command was successful
            print(f"EtherChannel information for group {group_no}:\n{output}")
            break

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to retrieve EtherChannel information for group {group_no}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
