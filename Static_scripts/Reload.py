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

# Initialize net_connect to None
net_connect = None

try:
    # Establish SSH connection to the device
    net_connect = ConnectHandler(**device)

    # Enter configuration mode 
    net_connect.config_mode()

    # Command to reload the switch
    command = "reload"

    # Send command to the device
    output = net_connect.send_command_timing(command)

    # Confirm the reload
    if "Proceed with reload? [confirm]" in output:
        output += net_connect.send_command_timing("\n")

    # Print success message
    print("The switch is reloading...")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except:
    print("Failed to reload the switch.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
