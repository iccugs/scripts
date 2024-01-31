#!/usr/bin/python3

import argparse

def prepend_host_to_lines(host, lines):
    return [f"{host}{line}" for line in lines]

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Prepend host to each line of a list.")
    parser.add_argument("--host", type=str, help="Host to prepend", required=True)
    parser.add_argument("--file", type=str, help="File containing the list", required=True)
    args = parser.parse_args()

    # Read lines from the file
    with open(args.file, 'r') as file:
        lines = file.readlines()

    # Prepend host to each line
    updated_lines = prepend_host_to_lines(args.host, lines)

    # Print the updated lines
    for line in updated_lines:
        print(line, end='')

if __name__ == "__main__":
    main()