#!/usr/bin/env python3
import requests
import argparse
import json

class WebArchiveUrlClass():

    def __init__(self, domain):
        self.web_archiveUrl = "http://web.archive.org/cdx/search?url=" + domain + "%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=100000&_=1547318148315"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def getUrls(self):
        r = requests.get(self.web_archiveUrl, headers=self.headers)
        html = r.text
        jsonObj = json.loads(html)
        filtered_rows = [row for row in jsonObj if not row[0].startswith("original")]
        return filtered_rows

def main():
    parser = argparse.ArgumentParser(description="Extracting URLs from http://web.archive.org")
    parser.add_argument("-d", "--domain", help="Specifies a single domain name")
    parser.add_argument("-l", "--list", help="Specifies a domain list file")
    parser.add_argument("-o", "--output", help="Specifies the output file for saving the results")

    args = parser.parse_args()

    if args.domain:
        domains = [args.domain]
    elif args.list:
        try:
            with open(args.list, "r") as file:
                domains = set(line.strip() for line in file if line.strip())
        except FileNotFoundError:
            print("The specified domain list file could not be found.")
            return
    else:
        print("Please specify a domain or domain list.")
        return

    output_file = args.output
    if output_file:
        with open(output_file, "w") as outfile:
            for domain in domains:
                wau = WebArchiveUrlClass(domain)
                for row in wau.getUrls():
                    outfile.write(row[0] + "\n")
    else:
        for domain in domains:
            wau = WebArchiveUrlClass(domain)
            for row in wau.getUrls():
                print(row[0])

if __name__ == "__main__":
    main()
