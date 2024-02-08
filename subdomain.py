#!/usr/bin/env python3

import requests
import sys
import argparse

def ascii_art():
    """Display the ASCII art for the tool."""
    art = """
    
       _____ _____  ______
      / ____|  __ \|  ____|
     | (___ | |  | | |__   _ __  _   _ _ __ ___
      \___ \| |  | |  __| | '_ \| | | | '_ ` _ \\
      ____) | |__| | |____| | | | |_| | | | | | |
     |_____/|_____/|______|_| |_|\__,_|_| |_| |_|
    
                      by Paradox
    
    """
    print(art)

def main(wordlist, domain):
    """Scan the given domain using subdomains from the wordlist."""
    
    # Headers to simulate a regular browser request.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Reading subdomains from the provided wordlist.
    with open(wordlist, 'r') as file:
        subDom = file.read().splitlines()

    # Check each subdomain for both http and https protocols.
    for sub in subDom:
        for protocol in ['http', 'https']:
            sDomain = f'{protocol}://{sub}.{domain}'

            # Send a GET request to the constructed subdomain.
            try:
                requests.get(sDomain, headers=headers, timeout=5)

            # Handle possible request exceptions.
            except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
                print(f'Cannot connect to: {sDomain}. Reason: {e}')

            # If request is successful, display the active subdomain.
            else:
                print(f'Domain exists: {sDomain}')

if __name__ == "__main__":
    # Display the ASCII art when the script starts.
    ascii_art()

    # Initialize the command-line argument parser.
    parser = argparse.ArgumentParser(description="Scan a domain for subdomains using a wordlist.")
    parser.add_argument('-w', '--wordlist', type=str, required=True, help="Path to the wordlist file containing subdomains to scan.")
    parser.add_argument('-d', '--domain', type=str, required=True, help="Domain name to scan for subdomains.") 
    
    # Parse the provided command-line arguments.
    args = parser.parse_args()

    # Start the scanning process.
    main(args.wordlist, args.domain)