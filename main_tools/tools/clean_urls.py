import argparse
import os
import logging
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse, parse_qs, urlencode
import urllib.parse as urlib

yellow_color_code = "\033[93m"
reset_color_code = "\033[0m"

colorama.init(autoreset=True)  

log_format = '%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)
logging.getLogger('').handlers[0].setFormatter(logging.Formatter(log_format))

HARDCODED_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json",
    ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"
]

def has_extension(url, extensions):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions

def clean_url(url):
    parsed_url = urlparse(url)
    
    try:
        port = int(parsed_url.port)
    except (ValueError, TypeError):
        port = None

    if (port == 80 and parsed_url.scheme == "http") or (port == 443 and parsed_url.scheme == "https"):
        cleaned_url = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
    else:
        cleaned_url = url

    return cleaned_url

def clean_urls(urls, extensions, placeholder):
    cleaned_urls = set()
    for url in urls:
        cleaned_url = clean_url(url)
        if not has_extension(cleaned_url, extensions):
            parsed_url = urlparse(cleaned_url)
            query_params = parse_qs(parsed_url.query)
            cleaned_params = {key: placeholder for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
            cleaned_urls.add(cleaned_url)
    return list(cleaned_urls)

def fetch_and_clean_urls(urls, extensions, stream_output, placeholder, output_file):
    logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Cleaning URLs...")
    cleaned_urls = clean_urls(urls, extensions, placeholder)
    logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Found {Fore.GREEN + str(len(cleaned_urls)) + Style.RESET_ALL} URLs after cleaning")
    logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Extracting URLs with parameters")
    
    with open(output_file, "w") as f:
        for url in cleaned_urls:
            if "?" in url:
                if stream_output:
                    print(url)
                f.write(url + "\n")
    
    logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Saved cleaned URLs to {Fore.CYAN + output_file + Style.RESET_ALL} file.")

def main():
    
    parser = argparse.ArgumentParser(description="Getting URLs with parameters and cleaning them.")
    parser.add_argument("-u", "--url-list", help="Specify a URL list for cleaning ", required=True)
    parser.add_argument("-s", "--stream", action="store_true", help="Show the urls on terminal.")
    parser.add_argument("-p", "--placeholder", help="Placeholder.", default="FUZZ")
    parser.add_argument("-o", "--output-file", help="Output file.", required=True)
    args = parser.parse_args()

    with open(args.url_list, "r") as f:
        urls = [line.strip() for line in f.readlines()]
        urls = [url for url in urls if url]  
        urls = list(set(urls)) 

    extensions = HARDCODED_EXTENSIONS

    fetch_and_clean_urls(urls, extensions, args.stream, args.placeholder, args.output_file)

if __name__ == "__main__":
    main()
