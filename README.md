# :honey_pot: Project Molasses-Masses

## :globe_with_meridians: Overview

Project Molasses-Masses is designed to provide a dynamically updated list of hosting providers from around the world. This list is based on the prefixes advertised as part of the BGP Autonomous System numbers.

Acknowledging that hosting providers themselves are not inherently problematic, some of their customers may have malicious intentions. Therefore, we adopt a "block first" approach, creating exceptions to allow legitimate traffic through as needed.

## :hammer_and_wrench: How It Works

The project uses a Python script (`molasses_masses.py`) to fetch and process IP prefixes associated with various hosting providers.

### Input

- The script reads from an input file named `hosting-providers-source.txt`.
- This file should contain a list of tuples with hosting provider names and their AS numbers.

### Output

The script generates output in the `data` directory:

1. :page_facing_up: `combined-v4.txt`: A list of all IPv4 prefixes ([View on Cloudflare](https://files.broda.io/molasses_masses/combined-v4.txt))
2. :page_facing_up: `combined-v6.txt`: A list of all IPv6 prefixes ([View on Cloudflare](https://files.broda.io/molasses_masses/combined-v6.txt))
3. :notebook_with_decorative_cover: Source data for the day

These files are published to Cloudflare for easy access and distribution.

## :rocket: Usage

To run the script:

```bash
python molasses_masses.py --if hosting-providers-source.txt --od data --verbose --combined --summarize
```

### Options:

- `--if`: Input file (required)
- `--od`: Output directory (required)
- `--verbose`: Enable verbose logging
- `--combined`: Create combined output files
- `--summarize`: Summarize IP addresses


## :warning: Disclaimer

This project is not meant to imply that all traffic from hosting providers is malicious. It's a tool for those who prefer a cautious approach to network traffic, allowing for precise control and whitelisting as needed.

## :handshake: Contributing

Contributions to Project Molasses-Masses are welcome! Please feel free to submit pull requests or open issues to improve the project.

