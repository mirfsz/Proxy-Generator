import requests
from lxml.html import fromstring
from random import shuffle
import logging
import sys
import time
from typing import List, Optional, Tuple
import itertools
import os

# Watermark
__author__ = "Irfan"
__version__ = "3.3"


# Set up logging to both file and console
def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("proxy_operations.log"),
                            logging.StreamHandler(sys.stdout)
                        ])


def fetch_proxies(limit: int = 100) -> List[str]:
    """Fetches a list of free proxies from sslproxies.org and ProxyScrape."""
    print(f"🔍 Fetching up to {limit} proxies...")

    proxies_list = []

    # Fetch from sslproxies.org
    url = 'https://sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)

    for i in parser.xpath('//tbody/tr')[:limit]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            ip = i.xpath('.//td[1]/text()')[0]
            port = i.xpath('.//td[2]/text()')[0]
            proxy = f"{ip}:{port}"
            proxies_list.append(proxy)

    # Fetch from ProxyScrape API (free endpoint)
    proxyscrape_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

    response = requests.get(proxyscrape_url)
    if response.status_code == 200:
        proxyscrape_proxies = response.text.strip().split('\r\n')
        proxies_list.extend(proxyscrape_proxies)

    shuffle(proxies_list)
    proxies_list = proxies_list[:limit]  # Limit the total number of proxies
    print(f"✅ Fetched {len(proxies_list)} proxies")
    return proxies_list


def check_if_sticky(proxy: str, num_requests: int = 3, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Checks if a proxy is sticky by making multiple requests and comparing the returned IP addresses.
    Returns a tuple: (is_sticky: bool, ip_address: Optional[str])
    """
    url = 'http://icanhazip.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }

    ip_addresses = set()
    try:
        for _ in range(num_requests):
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                ip_addresses.add(response.text.strip())
            time.sleep(1)  # Short delay between requests

        is_sticky = len(ip_addresses) == 1
        ip_address = ip_addresses.pop() if is_sticky else None
        return is_sticky, ip_address
    except Exception:
        return False, None


def validate_proxies(proxies_list: List[str], timeout: int = 5, proxy_type: str = "both") -> List[
    Tuple[str, bool, Optional[str]]]:
    """Tests proxies from the provided list and returns working ones based on the specified type."""
    print("🧪 Validating proxies and checking if they're sticky...")

    valid_proxies = []
    animation = itertools.cycle(['-', '/', '|', '\\'])

    for i, proxy in enumerate(proxies_list, 1):
        is_sticky, ip_address = check_if_sticky(proxy, timeout=timeout)

        if ip_address and (proxy_type == "both" or
                           (proxy_type == "sticky" and is_sticky) or
                           (proxy_type == "rotating" and not is_sticky)):
            valid_proxies.append((proxy, is_sticky, ip_address))
            proxy_status = "sticky" if is_sticky else "rotating"
            print(f"\r✅ Valid {proxy_status} proxy found: {proxy} (IP: {ip_address})" + " " * 20)
        else:
            print(f"\r❌ Invalid or unwanted proxy type: {proxy}" + " " * 20)

        sys.stdout.write(f"\r🔄 Testing proxy {i}/{len(proxies_list)} {next(animation)}")
        sys.stdout.flush()

    print(f"\n🎉 Validation complete! Found {len(valid_proxies)} working proxies of the requested type(s).")
    return valid_proxies


def export_proxies(proxies: List[Tuple[str, bool, Optional[str]]], filename: str = "working_proxies.txt"):
    """Exports working proxies to a file."""
    with open(filename, 'w') as f:
        f.write("Proxy,Is_Sticky,IP_Address\n")  # Header
        for proxy, is_sticky, ip_address in proxies:
            f.write(f"{proxy},{is_sticky},{ip_address}\n")
    print(f"📁 Exported {len(proxies)} working proxies to {filename}")


def display_menu():
    print("\n" + "=" * 50)
    print("🚀 Welcome to the Enhanced Proxy Generator v3.3 🚀")
    print("Created by Irfan")
    print("=" * 50)
    print("1. 🔍 Fetch and validate proxies")
    print("2. ℹ️  About")
    print("3. 🚪 Exit")
    print("=" * 50)
    return input("Please enter your choice (1-3): ")


def about():
    print("\n" + "=" * 50)
    print("🔧 Enhanced Proxy Generator v3.3")
    print(f"👨‍💻 Created by: {__author__}")
    print("=" * 50)
    print("🌟 Features:")
    print("   - Fetch free proxies from multiple sources")
    print("   - Validate proxies for functionality")
    print("   - Check if proxies are sticky or rotating")
    print("   - Filter proxies by type (sticky, rotating, or both)")
    print("   - Export working proxies to a file with detailed info")
    print("=" * 50)


def get_user_preferences():
    print("\n" + "=" * 50)
    print("📊 Proxy Search Preferences")
    print("=" * 50)

    limit = int(input("Enter the maximum number of proxies to fetch (default 100): ") or 100)
    timeout = int(input("Enter the timeout for proxy validation in seconds (default 5): ") or 5)

    print("\nProxy Type Options:")
    print("1. Sticky proxies only")
    print("2. Rotating proxies only")
    print("3. Both sticky and rotating proxies")

    while True:
        proxy_type_choice = input("Enter your choice (1-3): ")
        if proxy_type_choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please try again.")

    proxy_type_map = {'1': 'sticky', '2': 'rotating', '3': 'both'}
    proxy_type = proxy_type_map[proxy_type_choice]

    return limit, timeout, proxy_type


def main():
    setup_logging()
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    while True:
        choice = display_menu()

        if choice == '1':
            limit, timeout, proxy_type = get_user_preferences()

            proxies_list = fetch_proxies(limit)
            valid_proxies = validate_proxies(proxies_list, timeout, proxy_type)

            if valid_proxies:
                sticky_count = sum(1 for _, is_sticky, _ in valid_proxies if is_sticky)
                rotating_count = len(valid_proxies) - sticky_count

                print("\n" + "=" * 50)
                print("📊 Proxy Search Results")
                print("=" * 50)
                print(f"Total working proxies found: {len(valid_proxies)}")
                print(f"Sticky proxies: {sticky_count}")
                print(f"Rotating proxies: {rotating_count}")
                print("=" * 50)

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
            print("👋 Thank you for using Enhanced Proxy Generator. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()