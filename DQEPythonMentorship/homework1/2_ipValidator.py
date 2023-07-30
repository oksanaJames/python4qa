# encoding=utf-8
import re
import socket

# Create function for IP address validation using 1) library 're' and 2) socket.inet_aton


# 1.Validate ip address with re
def is_valid_ip_regex(ip_address):
    try:
        match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address)

        if not bool(match):
            print(f"The IP address {ip_address} is not valid")
            return False

        bytes = ip_address.split(".")

        for ip_byte in bytes:
            if int(ip_byte) < 0 or int(ip_byte) > 255:
                print(f"The IP address {ip_address} is not valid")
                return False
        print(f"The IP address {ip_address} is valid")
        return True
    except TypeError:  # not a valid address
        print("String is expected, but provided {}".format(type(ip_address)))


# 2. Validate ip address with socket.inet_aton
def is_valid_ip_socket(ip_address):
    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        print(f"The IP address {ip_address} is valid")
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip_address)
            print(f"The IP address {ip_address} is valid")
        except socket.error:
            print(f"The IP address {ip_address} is not valid")
            return False
        return ip_address.count('.') == 3
    except socket.error:  # not a valid address
        print(f"The IP address {ip_address} is not valid")
        return False
    except TypeError:  # not a valid address
        print("String is expected, but provided {}".format(type(ip_address)))
    return True


if __name__ == '__main__':
    is_valid_ip_regex('') # is False
    is_valid_ip_regex('192.168.0.1') # is True
    is_valid_ip_regex('0.0.0.1') # is True
    is_valid_ip_regex('10.100.500.32') # is False
    is_valid_ip_regex(700) # is False
    is_valid_ip_regex('127.0.1') # is True ???
    print("------------------------------------")
    is_valid_ip_socket('')  # is False
    is_valid_ip_socket('192.168.0.1')  # is True
    is_valid_ip_socket('0.0.0.1')  # is True
    is_valid_ip_socket('10.100.500.32')  # is False
    is_valid_ip_socket(700)  # is False
    is_valid_ip_socket('127.0.1')  # is True ???
    assert is_valid_ip_socket('127.0.1') is True