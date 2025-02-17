from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def show_snmp_contact():
    try:
        # Define device details
        device = {
            'device_type': 'cisco_ios',
            'host': input("Enter the IP address of the switch: "),
            'username': input("Enter your username: "),
            'password': input("Enter your password: "),
        }

        # Connect to the device
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('show snmp contact')
        print(output)

    except NetMikoTimeoutException:
        print("Connection timed out! Please check the IP address and try again.")
    except NetMikoAuthenticationException:
        print("Authentication failed! Please check your username and password and try again.")
    except Exception:
        print(f"An error occurred!")

show_snmp_contact()
