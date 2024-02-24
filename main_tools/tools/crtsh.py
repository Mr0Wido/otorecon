#!/usr/bin/env python3
import argparse
import requests
from bs4 import BeautifulSoup

class CrtShScraper:
    def __init__(self, domain):
        self.domain = domain

    def scrape_crtsh(self):
        url = f"https://crt.sh/?q=%25.{self.domain}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            tr_tags = soup.find_all("tr")
            crt_subdomains = []
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all("td")
                if len(td_tags) >= 6:
                    crtsh = td_tags[5].get_text(strip=True)
                    if "." in crtsh:
                        crt_subdomains.append(crtsh)
            return crt_subdomains

def save_to_file(subdomains, output_file):
    with open(output_file, 'w') as file:
        for subdomain in subdomains:
            file.write(subdomain + '\n')
            
def main():
    parser = argparse.ArgumentParser(description="Use the domain name to pull crt.sh data.")
    parser.add_argument("-d", "--domain", required=True, help="Domain name to search in crt.sh.")
    parser.add_argument("-o", "--output", help="Output file to save subdomains.")
    
    args = parser.parse_args()

    if not args.domain:
        parser.error("At least one of -d/--domain must be provided.")

    crtsh_scraper = CrtShScraper(args.domain)
    subdomains = crtsh_scraper.scrape_crtsh()

    if args.output:
        save_to_file(subdomains, args.output)
    else:
        for subdomain in subdomains:
            print(subdomain)

if __name__ == "__main__":
    main()
