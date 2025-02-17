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

    # Prompt user for LLDP timer value (in seconds)
    LLDP_timer = get_user_input("Enter the LLDP timer value (in seconds, e.g., '60'): ")

    # Command to configure LLDP timer
    command = f"LLDP timer {LLDP_timer}"

    # Enter configuration mode
    net_connect.config_mode()

    # Send command to the device
    output = net_connect.send_config_set([command])

    # Check if the input is invalid
    if '% Invalid input detected' in output:
        raise Exception
    else:
        # Print the output
        print(f"LLDP timer set to {LLDP_timer} seconds successfully")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print("Invalid timer value!")
finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
