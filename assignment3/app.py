import sys
import socket
import re
import redis

# Check for the correct number of arguments and validate NUM
if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) <= 0:
    print("Error: NUM must be a positive integer.")
    sys.exit(1)

NUM = int(sys.argv[1])

# connect to Redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
except redis.ConnectionError:
    print("Error: Could not connect to Redis server.")
    sys.exit(1)


# validate IPv4 address
def is_valid_ipv4(address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$' # regex to validate ip address (used chatgpt)
    if re.match(pattern, address):
        parts = address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

# Program to determine your IPv4 address (Method 1)
try:
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
except socket.gaierror:
    print("There was an error resolving the hostname.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# create a listening socket
listen_socket = socket.socket()
listen_socket.bind((socket.gethostname(), 8082))
listen_socket.listen(10)

print(f"Listening on {ipv4_address}:8082")

# accept new connections in a non-blocking manner
listen_socket.setblocking(False)

while True:
    address = input("Enter IPv4 ADDRESS (type zero to exit): ")
    if address == 'zero':
        break
    if not is_valid_ipv4(address):
        print("Error: Invalid IPv4 address.")
        continue

    try:
        with socket.socket() as s:
            s.connect((address, 8082))
            message = f"Hello, I am {ipv4_address} and my number is {NUM}"
            s.sendall(message.encode())

        # after sending, add the address to redis 'connections' list
        r.lpush('connections', address) #push to head of list

    except Exception as e:
        print(f"Error: Could not send message to {address}. Reason: {e}")

    # check for incoming connections
    try:
        conn, addr = listen_socket.accept()
        with conn:
            data = conn.recv(1024).decode()
            print(f"RECVD: {data}")
            ip_address = data.split()[3]  # assuming the message is formatted as expected
            r.rpush('connections', ip_address)  # add to the end of the list
    except BlockingIOError:
        continue  # no incoming connection

# close the listening socket when the program is exited
listen_socket.close()
