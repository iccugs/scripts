#!/usr/bin/python3

import re
import argparse
import sys
import pyfiglet

def parse_nmap_output(file_path, output_file=None):
    # Regular expression to match lines with open ports and services
    # This regex captures the port number followed by '/tcp' and the entire service description
    open_port_regex = re.compile(r"(\d+)/tcp\s+open\s+(.*)")

    # Read the file
    with open(file_path, 'r') as file:
        nmap_output = file.read()

    # Parsing the output
    open_ports = open_port_regex.findall(nmap_output)

    # Formatting the output
    header = "Port\t\tService"
    separator = "=" * 23
    formatted_output = f"{header}\n{separator}\n"
    for port, service in open_ports:
        formatted_output += f"{port}/tcp  \t{service}\n"

    # Output to console and optionally to file
    print(formatted_output)
    if output_file:
        with open(output_file, 'w') as out_file:
            out_file.write(formatted_output)

def main():
    # ASCII Art title
    ascii_art = pyfiglet.figlet_format("Nmap Output Parser")
    print(ascii_art, "\n\t\tBy: Paradox_Actual\n\n")

    parser = argparse.ArgumentParser(description='Parse Nmap output file.')
    parser.add_argument('file', help='Path to the Nmap output file', nargs='?')
    parser.add_argument('-o', '--output', help='Output file to write the results', default=None)

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Check if file argument is missing
    if not args.file:
        print("Error: Nmap output file path is required.\n")
        parser.print_help()
        sys.exit(1)

    parse_nmap_output(args.file, args.output)

if __name__ == "__main__":
    main()

