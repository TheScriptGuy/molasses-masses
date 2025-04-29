import argparse
import asyncio
import aiohttp
import ipaddress
import ast
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Dict, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "https://stat.ripe.net/data/announced-prefixes/data.json"

# Constants for excluded prefixes as sets (for O(1) lookup time)
EXCLUDED_PREFIXES = {
    "v4": {
        "0.0.0.0/0",  # Default IPv4
    },
    "v6": {
        "::/0",       # Default IPv6
    },
}


async def fetch_prefixes(session: aiohttp.ClientSession, provider: str, as_number: int, start_time: str) -> Tuple[str, int, List[str]]:
    """Fetch the list of prefixes for a given provider and AS number, filtering excluded prefixes."""
    params = {
        "resource": str(as_number),
        "starttime": start_time
    }
    try:
        async with session.get(API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                prefixes = [prefix["prefix"] for prefix in data.get("data", {}).get("prefixes", [])]

                result_prefixes = []
                for prefix in prefixes:
                    ip_version = categorize_ip(prefix)
                    if ip_version in ("v4", "v6") and prefix not in EXCLUDED_PREFIXES[ip_version]:
                        result_prefixes.append(prefix)
                    else:
                        logger.warning(f"Prefix {prefix} is part of excluded subnets for BGP AS{as_number}")
                return provider, as_number, result_prefixes
            else:
                logger.error(f"Error fetching data for {provider} (AS{as_number}): HTTP {response.status}")
                logger.error(f"Response content: {await response.text()}")
                return provider, as_number, []
    except Exception as e:
        logger.error(f"Exception while fetching data for {provider} (AS{as_number}): {str(e)}")
        return provider, as_number, []

def categorize_ip(ip: str) -> str:
    try:
        return "v4" if isinstance(ipaddress.ip_network(ip), ipaddress.IPv4Network) else "v6"
    except ValueError:
        logger.warning(f"Invalid IP address: {ip}")
        return "invalid"

def write_addresses_to_file(file_path: Path, addresses: List[str], summarize: bool = False) -> None:
    original_count = len(addresses)
    
    if summarize:
        addresses = summarize_addresses(addresses)
    
    with open(file_path, "w") as f:
        f.write("\n".join(addresses))
    
    if summarize:
        summarized_count = len(addresses)
        logger.info(f"Summarized {file_path} from {original_count} to {summarized_count} prefixes")
    else:
        logger.info(f"Created {file_path} with {original_count} prefixes")

def summarize_addresses(addresses: List[str]) -> List[str]:
    ip_networks = [ipaddress.ip_network(addr, strict=False) for addr in addresses]
    summarized = list(ipaddress.collapse_addresses(ip_networks))
    return [str(network) for network in summarized]

async def process_provider(session: aiohttp.ClientSession, provider: str, as_number: int, start_time: str, output_dir: Path, verbose: bool, summarize: bool) -> Dict[str, List[str]]:
    if verbose:
        logger.info(f"Processing {provider} (AS{as_number})")

    provider, as_number, prefixes = await fetch_prefixes(session, provider, as_number, start_time)

    if not prefixes:
        if verbose:
            logger.warning(f"No prefixes found for {provider} (AS{as_number})")
        return {"v4": [], "v6": []}

    v4_prefixes = []
    v6_prefixes = []

    for prefix in prefixes:
        if categorize_ip(prefix) == "v4":
            v4_prefixes.append(prefix)
        elif categorize_ip(prefix) == "v6":
            v6_prefixes.append(prefix)

    for ip_version, ip_list in [("v4", v4_prefixes), ("v6", v6_prefixes)]:
        if ip_list:
            filename = f"{provider}-AS{as_number}-{ip_version}.txt"
            file_path = output_dir / filename
            write_addresses_to_file(file_path, ip_list, summarize)

    return {"v4": v4_prefixes, "v6": v6_prefixes}

def parse_input_file(file_path: str) -> List[Tuple[str, int]]:
    with open(file_path, "r") as f:
        content = f.read()
    try:
        providers = ast.literal_eval(content)
        if not isinstance(providers, list) or not all(isinstance(item, tuple) and len(item) == 2 for item in providers):
            raise ValueError("Input file must contain a list of tuples")
        return providers
    except (SyntaxError, ValueError) as e:
        logger.error(f"Error parsing input file: {str(e)}")
        raise

async def main(input_file: str, output_dir: str, verbose: bool, combined: bool, summarize: bool) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    providers = parse_input_file(input_file)

    start_time = (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M")

    async with aiohttp.ClientSession() as session:
        tasks = [process_provider(session, provider, as_number, start_time, output_path, verbose, summarize and not combined) 
                 for provider, as_number in providers]
        results = await asyncio.gather(*tasks)

    if combined:
        combined_v4 = []
        combined_v6 = []
        for result in results:
            combined_v4.extend(result["v4"])
            combined_v6.extend(result["v6"])

        for ip_version, ip_list in [("v4", combined_v4), ("v6", combined_v6)]:
            if ip_list:
                filename = f"combined-{ip_version}.txt"
                file_path = output_path / filename
                write_addresses_to_file(file_path, ip_list, summarize)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and categorize IP prefixes for hosting providers")
    parser.add_argument("--if", dest="input_file", required=True, help="Input file containing provider tuples")
    parser.add_argument("--od", dest="output_dir", required=True, help="Output directory for prefix files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--combined", action="store_true", help="Create combined output files")
    parser.add_argument("--summarize", action="store_true", help="Summarize IP addresses")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    asyncio.run(main(args.input_file, args.output_dir, args.verbose, args.combined, args.summarize))
