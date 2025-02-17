from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def get_user_input(prompt, default=None):
    user_input = input(prompt)
    return user_input if user_input else default

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

    # Prompt user for the interface(s), rate limit, and burst interval
    interfaces = get_user_input("Enter the interface(s) you want to configure (e.g., Ethernet0/0, e0/0, or a range like e0/0-3): ")
    rate_limit = get_user_input("Enter the DAI rate limit (e.g., 15): ", default="15")
    burst_interval = get_user_input("Enter the burst interval (e.g., 1): ", default="1")

    # Command to configure the DAI rate limit and burst interval for the specified interface(s)
    commands = [
        f'interface range {interfaces}',
        f'ip arp inspection limit rate {rate_limit} burst interval {burst_interval}'
    ]

    # Enter configuration mode 
    net_connect.config_mode()

    # Send commands to the device
    output = net_connect.send_config_set(commands)

    # Check for errors in the output
    if "Invalid input detected" in output or "Incomplete command" in output:
        raise Exception()

    # Print success message
    print(f"Dynamic ARP Inspection rate limit has been set to {rate_limit} with burst interval {burst_interval} for interface(s) {interfaces} successfully!")

except NetMikoTimeoutException:
    print("Connection timed out! Please check the IP address and try again.")
except NetMikoAuthenticationException:
    print("Authentication failed! Please check your username and password and try again.")
except Exception:
    print(f"Failed to configure DAI rate limit for interface(s) {interfaces}.")

finally:
    # Close the connection if it was established
    if net_connect:
        net_connect.disconnect()
