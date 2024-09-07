import argparse
import ipaddress
import os
from typing import List, Union

def is_valid_ip_or_subnet(ip_or_subnet: str) -> bool:
    try:
        ipaddress.ip_network(ip_or_subnet, strict=False)
        return True
    except ValueError:
        return False

def ip_or_subnet_match(entry1: str, entry2: str) -> bool:
    try:
        network1 = ipaddress.ip_network(entry1, strict=False)
        network2 = ipaddress.ip_network(entry2, strict=False)
        return network1.overlaps(network2)
    except ValueError:
        return False

def search_file(file_path: str, search_entries: List[str], verbose: bool) -> List[str]:
    if verbose:
        print(f"Searching file: {file_path}")
    
    results = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not is_valid_ip_or_subnet(line):
                    if verbose:
                        print(f"Skipping invalid entry on line {line_number}: {line}")
                    continue
                
                for entry in search_entries:
                    if ip_or_subnet_match(entry, line):
                        results.append(f"{os.path.dirname(file_path)}/{os.path.basename(file_path)}: line {line_number}: {line}")
                        break  # Avoid duplicate results for the same line
    except Exception as e:
        if verbose:
            print(f"Error processing file {file_path}: {str(e)}")
    
    return results

def search_directory(directory: str, search_entries: List[str], verbose: bool) -> List[str]:
    if verbose:
        print(f"Searching directory: {directory}")
    
    results = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]  # Ignore hidden directories
        for file in sorted(files):
            if not file.startswith('.'):  # Ignore hidden files
                file_path = os.path.join(root, file)
                results.extend(search_file(file_path, search_entries, verbose))
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Search for IP addresses and subnets in files and directories.")
    parser.add_argument("--directory", help="Directory to search")
    parser.add_argument("--file", help="File to search")
    parser.add_argument("--search", required=True, help="Comma-separated list of IP addresses and/or subnets to search for")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if not (args.directory or args.file):
        parser.error("At least one of --directory or --file must be provided")

    search_entries = args.search.split(',')
    
    for entry in search_entries:
        if not is_valid_ip_or_subnet(entry):
            parser.error(f"Invalid IP address or subnet in search entries: {entry}")

    results = []

    if args.directory:
        results.extend(search_directory(args.directory, search_entries, args.verbose))
    
    if args.file:
        results.extend(search_file(args.file, search_entries, args.verbose))

    for result in results:
        print(result)

if __name__ == "__main__":
    main()
