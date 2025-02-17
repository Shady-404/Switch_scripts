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

    # Command to show the ARP table
    command = "show ip arp"

    # Send command to the device and capture the output
    output = net_connect.send_command(command)

    # Print the ARP table
    print("ARP Table:")
    print(output)

    # Close the connection
    net_connect.disconnect()

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"An error occurred!")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
