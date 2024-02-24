#!/usr/bin/env python3
import requests
import json
import threading
import queue
import argparse

class CommonCrawlDataRetrieval:

    def __init__(self, domain):
        self.domain = domain
        self.visited_urls = set()
        self.queue = queue.Queue()

    def get_indexes(self):
        index_url = "https://index.commoncrawl.org/collinfo.json"
        response = requests.get(index_url)
        index_data = json.loads(response.text)

        for index in index_data:
            self.queue.put(index['id'])

    def get_index_data(self, index_id):
        try:
            common_crawl_url = f"http://index.commoncrawl.org/{index_id}-index?url={self.domain}/*&output=json"
            response = requests.get(common_crawl_url)
            data = response.text.split("\n")[:-1]

            for entry in data:
                url = json.loads(entry)['url']
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    print(url)
        except:
            pass

    def worker(self):
        while True:
            index_id = self.queue.get()
            self.get_index_data(index_id)
            self.queue.task_done()

    def start(self, num_threads=100):
        self.get_indexes()

        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()

        self.queue.join()

def main():
    parser = argparse.ArgumentParser(description="Common Crawl Data Retrieval Tool")
    parser.add_argument("-d", "--domain", help="Domain Name; Example: test.com")
    parser.add_argument("-l", "--list", help="Domain list file name")

    args = parser.parse_args()

    if not args.domain and not args.list:
        parser.error("You must specify either a domain or a domain list file.")

    if args.domain:
        domain = args.domain
        cc = CommonCrawlDataRetrieval(domain)
        cc.start()
    elif args.list:
        try:
            with open(args.list, "r") as file:
                domains = set(line.strip() for line in file if line.strip())
                for domain in domains:
                    cc = CommonCrawlDataRetrieval(domain)
                    cc.start()
        except FileNotFoundError:
            print("The specified domain list file was not found.")

if __name__ == "__main__":
    main()
