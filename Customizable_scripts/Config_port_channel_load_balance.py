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

    # Prompt user for the port-channel load-balance method
    load_balance_method = get_user_input("Enter the port-channel load-balance method (e.g., src-mac, dst-mac, src-dst-ip, etc.): ")

    # Commands to configure port-channel load balancing
    commands = [
        f"port-channel load-balance {load_balance_method}"
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for common errors in the output
    if '% Invalid input detected' in output:
        raise Exception
    elif '% Incomplete command' in output:
        print("Incomplete command. Please check the command syntax and try again.")
    elif '% Ambiguous command' in output:
        print("Ambiguous command. Please provide more specific input.")
    else:
        # Print the output if no errors are found
        print(f"Port-channel load-balance method set to {load_balance_method}")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to set port-channel load-balance method.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()