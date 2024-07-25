import requests
from lxml.html import fromstring
from random import shuffle
import logging
import sys
import time
from typing import List, Optional
import itertools
import os

# Watermark
__author__ = "Irfan"
__version__ = "2.0"


# Set up logging to both file and console
def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("proxy_operations.log"),
                            logging.StreamHandler(sys.stdout)
                        ])


def fetch_proxies(limit: int = 100) -> List[str]:
    """Fetches a list of free proxies from sslproxies.org."""
    print(f"🔍 Fetching up to {limit} proxies...")

    url = 'https://sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)

    proxies_list = []
    for i in parser.xpath('//tbody/tr')[:limit]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            ip = i.xpath('.//td[1]/text()')[0]
            port = i.xpath('.//td[2]/text()')[0]
            proxy = f"{ip}:{port}"
            proxies_list.append(proxy)

    shuffle(proxies_list)
    print(f"✅ Fetched {len(proxies_list)} proxies")
    return proxies_list


def validate_proxies(proxies_list: List[str], timeout: int = 5) -> List[str]:
    """Tests proxies from the provided list and returns all working ones."""
    print("🧪 Validating proxies...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = 'http://icanhazip.com'

    valid_proxies = []
    animation = itertools.cycle(['-', '/', '|', '\\'])

    for i, proxy in enumerate(proxies_list, 1):
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                valid_proxies.append(proxy)
                print(f"\r✅ Valid proxy found: {proxy}" + " " * 20)
            else:
                print(f"\r❌ Invalid proxy: {proxy}" + " " * 20)
        except Exception:
            print(f"\r❌ Failed proxy: {proxy}" + " " * 20)

        sys.stdout.write(f"\r🔄 Testing proxy {i}/{len(proxies_list)} {next(animation)}")
        sys.stdout.flush()

    print(f"\n🎉 Validation complete! Found {len(valid_proxies)} working proxies.")
    return valid_proxies


def export_proxies(proxies: List[str], filename: str = "working_proxies.txt"):
    """Exports working proxies to a file."""
    with open(filename, 'w') as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    print(f"📁 Exported {len(proxies)} working proxies to {filename}")


def display_menu():
    print("\n" + "=" * 40)
    print("🚀 Welcome to the Proxy Generator v2.0 🚀")
    print("Created by Irfan")
    print("=" * 40)
    print("1. 🔍 Fetch and validate proxies")
    print("2. ℹ️  About")
    print("3. 🚪 Exit")
    return input("Please enter your choice (1-3): ")


def about():
    print("\n" + "=" * 40)
    print("🔧 Proxy Generator v2.0")
    print(f"👨‍💻 Created by: {__author__}")
    print("🌟 Features:")
    print("   - Fetch free proxies from sslproxies.org")
    print("   - Validate proxies for functionality")
    print("   - Export working proxies to a file")
    print("=" * 40)


def main():
    setup_logging()
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    while True:
        choice = display_menu()

        if choice == '1':
            limit = int(input("Enter the maximum number of proxies to fetch (default 100): ") or 100)
            timeout = int(input("Enter the timeout for proxy validation in seconds (default 5): ") or 5)

            proxies_list = fetch_proxies(limit)
            valid_proxies = validate_proxies(proxies_list, timeout)

            if valid_proxies:
                export = input("Do you want to export the working proxies to a file? (y/n): ").lower()
                if export == 'y':
                    filename = input("Enter the filename (default: working_proxies.txt): ") or "working_proxies.txt"
                    export_proxies(valid_proxies, filename)
            else:
                print("❌ No working proxies found. Please try again with different parameters.")

            input("\nPress Enter to return to the main menu...")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

        elif choice == '2':
            about()
            input("\nPress Enter to return to the main menu...")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

        elif choice == '3':
            print("👋 Thank you for using Proxy Generator. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()