#!/usr/bin/env python3
import argparse
import requests

def get_archive_data(domain):
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()

    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="Use the domain name to retrieve data for web.archive.org.")
    parser.add_argument("-d", "--domain", help="Using the domain name.")
    parser.add_argument("-l", "--list", help="Using the URL list.")
    args = parser.parse_args()
    list = args.list

    if args.domain:
        archive_data = get_archive_data(args.domain)
        if archive_data:
            for item in archive_data:
                print(item)

    elif args.list:
        with open(list, 'r') as url_file:
            urls = set(line.strip() for line in url_file if line.strip())
        
        for url in urls:
            archive_data = get_archive_data(url)
            if archive_data is None:
                continue
            for item in archive_data:
                print(item)

if __name__ == "__main__":
    main()
