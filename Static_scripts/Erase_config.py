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

    # Command to erase the startup configuration
    output = net_connect.send_command_timing("write erase")

    # Handle the confirmation prompt
    if 'confirm' in output.lower():
        output += net_connect.send_command_timing("\n")

    # Print success message
    print("Startup configuration has been erased successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Failed to erase the startup configuration.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()

