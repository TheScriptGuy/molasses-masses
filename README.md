# :honey_pot: Project Molasses-Masses

## :globe_with_meridians: Overview

Project Molasses-Masses is designed to provide a dynamically updated list of hosting providers from around the world. This list is based on the prefixes advertised as part of the BGP Autonomous System numbers.

Acknowledging that hosting providers themselves are not inherently problematic, some of their customers may have malicious intentions. Therefore, we adopt a "block first" approach, creating exceptions to allow legitimate traffic through as needed.

This project is currently tracking `15158` IPv4 Subnets and `2306` IPv6 Subnets.

## :hammer_and_wrench: How It Works

The project uses a Python script (`molasses_masses.py`) to fetch and process IP prefixes associated with various hosting providers.

### Input

- The script reads from an input file named `hosting-providers-source.txt`.
- This file should contain a list of tuples with hosting provider names and their AS numbers.

### Output

:warning:
The links below on Cloudflare will be removed on *30 June 2025* and replaced with links that require a key.

The script generates output in the `data` directory:

1. :page_facing_up: `combined-v4.txt`: A list of all IPv4 prefixes ([View on Cloudflare](https://files.broda.io/molasses_masses/combined-v4.txt))
2. :page_facing_up: `combined-v6.txt`: A list of all IPv6 prefixes ([View on Cloudflare](https://files.broda.io/molasses_masses/combined-v6.txt))

These files are published to Cloudflare for easy access and distribution.

## :email: To Access

To access the IPv4 and IPv6 prefixes available for download, please send an email to `get-api-key <at> mm.broda.io` with the following information:
1. Name:
2. Email:
3. Purpose: Lab/Home user
4. Company (if applicable) and number of users:

(For company/corporate use, there is a licensing cost associated. Include interest and pricing will be sent through) 

The email will be where the usage keys are sent to along with instructions on how to use.

# IP and Subnet Search Tool

This Python script searches for an exact match or the presence of IP addresses or subnets within files or directories containing a list of IPs/subnets. It's designed to help you quickly locate IP addresses or subnets from large datasets.

## :arrow_forward: Usage

To use this script, you need to provide either a directory or a file to search, along with the IP addresses or subnets you want to search for.

### Command-line Arguments

- `--directory` : Directory to search for files containing IP addresses or subnets.
- `--file` : Specific file to search.
- `--search` : Comma-separated list of IP addresses and/or subnets to search for. **(Required)**
- `--verbose` : Enable verbose output for detailed processing information.

### Examples

#### Example 1: Search a Directory

To search all files in the `data` directory for the IP address `192.100.0.0/24`, run:

```bash
python script.py --directory data --search 192.100.0.0/24
```

#### Example 2: Search a Specific File

To search a specific file, such as `data/2024-09-09/global-communications-net-AS12615-v4.txt`, for multiple IP addresses or subnets, run:
```bash
python script.py --file data/2024-09-09/global-communications-net-AS12615-v4.txt --search 192.100.1.0/24,100.0.0.0/8
```

#### Example 3: Search with Verbose Output

To search the data directory with verbose output, run:
```bash
python script.py --directory data --search 192.100.1.0/24 --verbose
```

#### :page_facing_up: Example Output
When running the script with a search query, you might see output similar to the following:
```text
Searching directory: data
Searching file: data/2024-09-09/global-communications-net-AS12615-v4.txt
Skipping invalid entry on line 5: InvalidSubnet/33
data/2024-09-09/global-communications-net-AS12615-v4.txt: line 10: 192.100.1.0/24
data/2024-09-09/amanah-tech-AS32489-v4.txt: line 15: 100.0.0.0/8
...
```

### :bulb: Important Notes

    At least one of --directory or --file must be provided. The script requires at least one input source to search.
    The --search argument is required and should contain a comma-separated list of valid IP addresses or subnets.
    The script skips invalid IP addresses or subnets found in files and will display a message if the --verbose flag is enabled.

### :wrench: Additional Information

    If the --directory argument is provided, the script will recursively search through all files within the directory (excluding hidden files and directories).
    If the --file argument is used, only that specific file will be searched.
    The search is performed using Python's ipaddress module, which checks for both exact matches and subnet overlaps.


## :warning: Disclaimer

This project is not meant to imply that all traffic from hosting providers is malicious. It's a tool for those who prefer a cautious approach to network traffic, allowing for precise control and whitelisting as needed. If you leverage cloud hosted services, then it is up to you to filter out your applicable IP addresses/subnets from the list. I cannot be held liable for any actions of this block list.

## :fire: Shorewall Blocklist

I have created a bash script `molasses-masses-shorewall.sh` that will help download the files and update shorewall rules to reflect the list of subnets that should be blocked. It should only update the list of iptables if the files hosted on Cloudflare have been updated.

## :handshake: Contributing

Contributions to Project Molasses-Masses are welcome! Please feel free to submit pull requests or open issues to improve the project.
