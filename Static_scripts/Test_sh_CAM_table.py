from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

import sys

def validate_ip(ip):
    # Validate the IP address
    return ip == "192.168.1.100"

def validate_credentials(username, password):
    # Validation for demonstration purposes
    return username == "Shady" and password == "123"

ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

if not validate_ip(ip):
    print("Invalid IP address")
elif not validate_credentials(username, password):
    print("Invalid username or password")


device = {
    'device_type': 'cisco_ios',
    'host': "192.168.1.100",
    'username': "Shady",
    'password': "123" }

net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Command to show the MAC address table
    command = "show mac address-table"

    # Send command to the device and capture the output
    output = net_connect.send_command(command)

    # Print the MAC address table
    # print("MAC Address Table:")
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
