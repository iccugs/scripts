#!/usr/bin/python3

import subprocess
import os
import pty
import select
import tempfile

def read_ports(file_path):
    """Read ports from the given file and return them as a list of integers."""
    with open(file_path, 'r') as file:
        return sorted([int(line.strip()) for line in file])

def ssh_connect(ip, port, known_hosts_file):
    """Use pty to run the SSH command in a pseudo-terminal and capture its output."""
    master, slave = pty.openpty()  # Open a pseudo-terminal
    ssh_cmd = ["ssh", ip, "-o", "HostKeyAlgorithms=+ssh-rsa", 
               "-o", "StrictHostKeyChecking=no", "-o", f"UserKnownHostsFile={known_hosts_file}", 
               "-p", str(port)]
    
    # Run SSH command in a subprocess with the pseudo-terminal
    proc = subprocess.Popen(ssh_cmd, stdin=slave, stdout=slave, stderr=slave, text=True)
    os.close(slave)

    # Wait for the response
    response = ""
    while True:
        r, w, e = select.select([master], [], [], 5)
        if master in r:
            try:
                output = os.read(master, 1024).decode('utf-8')
                response += output
                if output.strip():  # Break if any response is received
                    break
            except OSError:
                break

    os.close(master)
    proc.terminate()
    return response

def find_ssh_port(ports, ip):
    """Find the correct SSH port using a binary search algorithm."""
    low = 0
    high = len(ports) - 1

    # Create a temporary file for known hosts
    with tempfile.NamedTemporaryFile() as temp_known_hosts:
        while low <= high:
            mid = (low + high) // 2
            port = ports[mid]
            response = ssh_connect(ip, port, temp_known_hosts.name)

            print(f"Port {port}: Server response - '{response.strip()}'")  # Logging response

            if "You've found the real service" in response:
                return port  # Correct port found
            elif "Lower" in response:
                low = mid + 1  # Search in higher half
            elif "Higher" in response:
                high = mid - 1  # Search in lower half

    return None  # Port not found

# Example usage
ports = read_ports('ports_list.txt')  # Replace with your file path
ip = '10.10.10.10'  # Replace with the SSH server's IP address

# Call the function to find the correct SSH port
correct_port = find_ssh_port(ports, ip)

if correct_port is not None:
    print(f"The correct SSH port is: {correct_port}")
else:
    print("Failed to find the correct SSH port.")
