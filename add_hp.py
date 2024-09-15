#!/usr/bin/env python3
"""
add_hp.py - Add Hosting Provider Script

This script adds a new hosting provider entry to the hosting-providers-source.txt file.
It accepts two mandatory arguments: "name" and "as" (Autonomous System number).

Usage:
    python add_hp.py <name> <as>

Arguments:
    name: Name of the hosting provider (alphanumeric, hyphens, and underscores allowed)
    as: Autonomous System number (positive integer)

The script will append the new entry to the file, check for duplicates based on the AS number,
and provide feedback on the operation's success.

Author: TheScriptGuy
Date:   2024-09-15
"""

import sys
import re
import os
import ast

FILE_NAME = "hosting-providers-source.txt"

def validate_arguments(args):
    """
    Validate the command-line arguments.

    Args:
        args (list): List of command-line arguments.

    Returns:
        tuple: (name, as_number) if valid, None otherwise.
    """
    if len(args) != 3:
        print("Error: Exactly two arguments (name and AS number) are required.")
        return None

    name = args[1]
    as_number = args[2]

    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        print("Error: Name must contain only alphanumeric characters, hyphens, and underscores.")
        return None

    try:
        as_number = int(as_number)
        if as_number <= 0:
            raise ValueError
    except ValueError:
        print("Error: AS number must be a positive integer.")
        return None

    return name, as_number

def read_file_content(file_name):
    """
    Read the content of the file and return it as a list of tuples.

    Args:
        file_name (str): Name of the file to read.

    Returns:
        list: List of tuples containing the hosting provider entries.
    """
    if not os.path.exists(file_name):
        return []

    with open(file_name, 'r') as file:
        content = file.read().strip()
        if not content:
            return []

        # Remove brackets and split into lines
        lines = content.strip('[]').split('\n')
        
        # Parse each line into a tuple using ast.literal_eval
        return [ast.literal_eval(line.strip().rstrip(',')) for line in lines if line.strip()]

def write_file_content(file_name, content):
    """
    Write the content to the file.

    Args:
        file_name (str): Name of the file to write.
        content (list): List of tuples to write to the file.
    """
    with open(file_name, 'w') as file:
        file.write('[\n')
        for i, item in enumerate(content):
            if i < len(content) - 1:
                file.write(f"{item},\n")
            else:
                file.write(f"{item}\n")
        file.write(']\n')

def add_hosting_provider(name, as_number):
    """
    Add a new hosting provider to the file.

    Args:
        name (str): Name of the hosting provider.
        as_number (int): Autonomous System number.

    Returns:
        bool: True if the addition was successful, False otherwise.
    """
    content = read_file_content(FILE_NAME)

    # Check for duplicates
    for index, (_, existing_as) in enumerate(content):
        if existing_as == as_number:
            print(f"Error: Duplicate AS number found on line {index + 2}.")
            return False

    # Append new entry
    content.append((name, as_number))
    write_file_content(FILE_NAME, content)
    return True

def main():
    """
    Main function to handle the script's execution.
    """
    args = validate_arguments(sys.argv)
    if not args:
        sys.exit(1)

    name, as_number = args
    if add_hosting_provider(name, as_number):
        print(f"Successfully added ({name}, {as_number}) to {FILE_NAME}")
        content = read_file_content(FILE_NAME)
        print(f"Total entries in the list: {len(content)}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
