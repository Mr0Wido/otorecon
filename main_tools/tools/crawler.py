#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import argparse
import os
import sys


sys.stderr = open(os.devnull, 'w')
# ...existing code...

class DiscoveryWebCrawler:
    def __init__(self, domain, output_file):
        self.domain = domain
        self.urls = set()
        self.output_file = output_file

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == urlparse(self.domain).netloc

    def crawl_url(self, crawl_url):
        try:
            response = requests.get(crawl_url, verify=False, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    href = urljoin(self.domain, href)
                    if self.is_valid_url(href):
                        self.urls.add(href)
        except Exception as e:
            pass

    def start(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.crawl_url, [self.domain])
def save_results_to_file(output_file, urls):
    with open(output_file, "w") as file:
        for url in urls:
            file.write(url + '\n')


def print_results(urls):
    for url in urls:
        print(url)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Domain Name; EX: https://test.com")
    parser.add_argument("-l", "--list", help="The domain list;")
    parser.add_argument("-o", "--output_file", help="Output file to save the URLs")
    args = parser.parse_args()

    if args.domain:
        domain_name = args.domain
        domain = f'https://{domain_name}'
        web_crawler = DiscoveryWebCrawler(domain, args.output_file)
        web_crawler.start()
        if args.output_file:
            save_results_to_file(args.output_file, web_crawler.urls)
        else:
            print_results(web_crawler.urls)

    elif args.list:
        file_name = args.list
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                domains = [f'https://{line.strip()}' for line in f.readlines()]

            web_crawlers = []
            for domain in domains:
                crawler = DiscoveryWebCrawler(domain, args.output_file)
                web_crawlers.append(crawler)

            with ThreadPoolExecutor(max_workers=10) as executor:
                for web_crawler in web_crawlers:
                    executor.submit(web_crawler.start)

            all_urls = set()
            for web_crawler in web_crawlers:
                all_urls.update(web_crawler.urls)

            if args.output_file:
                save_results_to_file(args.output_file, all_urls)
            else:
                print_results(all_urls)

        else:
            print(f"'{file_name}' file not found.")
    else:
        print("Please specify a domain or file.")

if __name__ == "__main__":
    main()