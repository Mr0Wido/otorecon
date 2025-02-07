#!/usr/bin/env python3
import requests
import argparse
import json
import concurrent.futures

class WebArchiveUrlClass:
    def __init__(self, domain):
        self.web_archiveUrl = (
            "https://web.archive.org/cdx/search?url=" + domain +
            "%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=100000&_=1547318148315"
        )
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def getUrls(self):
        try:
            r = requests.get(self.web_archiveUrl, headers=self.headers, timeout=10)
            r.raise_for_status()
            jsonObj = json.loads(r.text)
            return [row[0] for row in jsonObj if not row[0].startswith("original")]
        except (requests.RequestException, json.JSONDecodeError) as e:
            return []

def process_domain(domain, output_file=None):
    wau = WebArchiveUrlClass(domain)
    urls = wau.getUrls()

    if output_file:
        with open(output_file, "a") as outfile:  # Append mode to avoid overwriting
            for url in urls:
                outfile.write(url + "\n")
    else:
        for url in urls:
            print(url)

def main():
    parser = argparse.ArgumentParser(description="Extracting URLs from http://web.archive.org")
    parser.add_argument("-d", "--domain", help="Specifies a single domain name")
    parser.add_argument("-l", "--list", help="Specifies a domain list file")
    parser.add_argument("-o", "--output", help="Specifies the output file for saving the results")

    args = parser.parse_args()

    domains = []
    if args.domain:
        domains.append(args.domain)
    elif args.list:
        try:
            with open(args.list, "r") as file:
                domains = list(set(line.strip() for line in file if line.strip()))
        except FileNotFoundError:
            print("The specified domain list file could not be found.")
            return
    else:
        print("Please specify a domain or domain list.")
        return

    output_file = args.output

    # Çoklu iş parçacığı (Threading) kullanımı
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_domain, domain, output_file): domain for domain in domains}

        for future in concurrent.futures.as_completed(futures):
            domain = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {domain}: {e}")

if __name__ == "__main__":
    main()
