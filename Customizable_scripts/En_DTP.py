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

    # Prompt user for the interface or range of interfaces
    interfaces = get_user_input("Please enter the interface (e.g., Ethernet0/0, e0/0, or a range like e0/0-3): ")

    # Prompt user for the DTP mode (desirable or auto) 
    dtp_mode = get_user_input("Please enter the DTP mode (desirable or auto): ").strip().lower() 
    # Validate the DTP mode 
    if dtp_mode not in ['desirable', 'auto']: raise ValueError("Invalid DTP mode! Please enter 'desirable' or 'auto'.")
    # Commands to configure the interface as a switchport and enable DTP
    commands = [
        f"interface range {interfaces}",
        "no switchport nonegotiate",
        f"switchport mode dynamic {dtp_mode}",
        "end"
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output or "Command rejected" in output:
        raise Exception()

# Print success message 
    print(f"DTP mode '{dtp_mode}' has been set on interface(s) {interfaces} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except ValueError as ve:
    print(str(ve))
except Exception:
    print(f"Failed to enable DTP on interface(s) {interfaces}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()