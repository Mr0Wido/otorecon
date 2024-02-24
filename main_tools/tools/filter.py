#!/usr/bin/env python3
import argparse
import asyncio
import requests
import colorama
from urllib.parse import urlparse
from sys import exit

colorama.init(autoreset=True)

class SubdomainStatusFilter:
    def __init__(self, domains, status_codes):
        self.domains = domains
        self.status_codes = status_codes

    async def validate_domain(self, domain, protocol):
        url = f"{protocol}{domain}"
        try:
            response = await asyncio.to_thread(requests.get, url, timeout=1)
            status_code = response.status_code
        except requests.RequestException as e:
            status_code = None

        return url, status_code

    async def filter_domains(self):
        valid_protocols = ['http://', 'https://']

        for domain in self.domains:
            for protocol in valid_protocols:
                result = await self.validate_domain(domain, protocol)
                self.print_result(result)

    def print_result(self, result):
        url, status_code = result
        if status_code is not None:
            status_code_str = str(status_code)
            colored_status_code_str = colorama.Fore.GREEN + status_code_str + colorama.Style.RESET_ALL
        else:
            colored_status_code_str = colorama.Fore.RED + "-" + colorama.Style.RESET_ALL

        if self.status_codes[0] == "all": 
            print(f"{url} ({colored_status_code_str})")
        else:
            if str(status_code) in self.status_codes:
                print(f"{url} ({colored_status_code_str})")

    def save_result_to_file(self, result, output_file):
        url, status_code = result
        if status_code is not None:
            status_code_str = str(status_code)
        else:
            status_code_str = "-"
        with open(output_file, "a") as file:
            file.write(f"{url} ({status_code_str})\n")

def main():
    parser = argparse.ArgumentParser(description="Subdomain Status Code Filter Tool")
    parser.add_argument("-l", "--domains_file", help="Path to the domains list file")
    parser.add_argument("-d", "--domain", help="Single domain to filter (e.g., example.com)")
    parser.add_argument("-sc", "--status_codes", required=True, nargs="+", help="List of status codes to filter (e.g., 200 404 500) or 'all'")
    parser.add_argument("-o", "--output_file", help="Path to the output file where results will be saved")

    args = parser.parse_args()

    domains = []

    if args.domains_file:
        with open(args.domains_file, "r") as file:
            domains = file.read().splitlines()
    elif args.domain:
        domains.append(args.domain)
    else:
        print("Either -l or -d option must be provided.")
        exit(1)

    subdomain_filter = SubdomainStatusFilter(domains, args.status_codes)
    asyncio.run(subdomain_filter.filter_domains())

    if args.output_file:
        if args.output_file:
            with open(args.output_file, "w") as file:
                pass  # Boş dosya oluştur

        for domain in domains:
            for protocol in ['http://', 'https://']:
                result = asyncio.run(subdomain_filter.validate_domain(domain, protocol))
                subdomain_filter.save_result_to_file(result, args.output_file)

if __name__ == "__main__":
    main()
