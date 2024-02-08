#!/usr/bin/env python3

import pyfiglet
import socket
import time
import sys
import argparse

def fuzz_target(ip, port, timeout, buffer):
    for string in buffer:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))
            server_response = s.recv(1024)
            print(f"Server Response: {server_response}")
            print(f"Fuzzing with {len(string)} bytes")
            s.send(bytes(string + "\r\n", "latin-1"))
            server_response = s.recv(1024)
            print(f"Server Response: {server_response}")
            s.close()
            time.sleep(1)
        except socket.error as e:
            print(f"Could not connect to {ip}:{port}")
            print(f"Fuzzing crashed at {len(string)} bytes")
            print(f"Exception: {str(e)}")
            sys.exit(0)

def generate_payload(start_size, max_size, increment):
    buffer = []
    while start_size < max_size:
        buffer.append("A" * start_size)
        start_size += increment
    return buffer

def main():
    asciiText = "Dynamic Fuzzer"
    asciiArt = pyfiglet.figlet_format(asciiText, font='digital')
    print(asciiArt)
    
    parser = argparse.ArgumentParser(description="Dynamic fuzzer for vulnerable application.")
    parser.add_argument("ip", type=str, help="IP address of target")
    parser.add_argument("port", type=int, help="Port number of target")
    args = parser.parse_args()
    
    ip = args.ip
    port = args.port
    timeout = 5
    
    buffer = generate_payload(100, 4000, 100)
    fuzz_target(ip, port, timeout, buffer)

if __name__ == "__main__":
    main()