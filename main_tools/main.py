# main.py
import colorama
import subprocess
from tqdm.autonotebook import tqdm
import argparse
from bs4 import BeautifulSoup
import os
import sys
import json
colorama.init()

blue = colorama.Fore.BLUE
red = colorama.Fore.RED
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
reset = colorama.Fore.RESET

from main_tools.subdomain_scan import subdomain_scan
from main_tools.crawler_scan import crawler_scan
from main_tools.dirsearch_scan import dirsearch_scan
from main_tools.filter_scan import filter_subs_scan
from main_tools.basic_info import basic_info_scan
from main_tools.get_screenshot import get_screenshot

def parser_arguments():
    parser = argparse.ArgumentParser(description='subdomain discovery tools')
    parser.add_argument('-bs', '--basic_scan', help='Basic Information Scan; Specify tools to run or use "all" to run all tools', nargs = '*', choices = ['dnmasscan', 'whatweb', 'google_dork', 'github_dork', 'whois' ,'all'], default=None)
    parser.add_argument('-subs', '--subdomain_scan',help = 'Specify subdomain tools to run or use "all"',nargs = '*', choices = ['subfinder', 'assetfinder',  'findomain', 'crtsh','theharvester', 'cero', 'scilla', 'dnsx', 'shuffledns', 'dnsgen', 'altdns', 'gau' ,'all'], default=None)
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-f', '--file', help='File containing domain names to scan', action='store', default=None, required=False)    
    parser.add_argument('-os', '--out_of_scope', help='Out-of-scope domains file path', default=None, required=False)
    parser.add_argument('-cs', '--crawler_scan', help='Pulling URLs from crawler tools', nargs='*', choices = ['crawler' , 'waybackurl','gau', 'katana', 'getjs', 'hakrawler', 'all'], default=None)
    parser.add_argument('-cl', '--crawler_list', help='Crawler list for the crawler scan', default=None, required=False)
    parser.add_argument('-cp', '--crawler_param', help='Crawler result parameter', action='store_true', required=False)
    parser.add_argument('-ds', '--dirsearch_scan', help='Directory Search', nargs='*', choices = ['rd1000', 'raft', 'dirm2_3', 'dirsearch', 'all'], default=None)
    parser.add_argument('-dl', '--dirsearch_list', help='Subdomain list for the directory scan', default=None, required=False)
    parser.add_argument('-fl', '--filter_list', help='Domain,URL lists for filter', default=None, required=False)
    parser.add_argument('-sc', '--status_codes', help='Status codes for filter -sc 200,404,500', default=None, required=False)
    parser.add_argument('-p', '--ports', help='Ports for filter -p 80,443,8080', default=None, required=False)
    parser.add_argument('-clr','--clear_protocol_status_code', help='Clear protocols and status codes', action='store_true', required=False)  
    parser.add_argument('-gsc', '--get_screenshot', help='URL file for gowitness', action='store', default=None)
    return parser.parse_args()

def banner():
    print(f"""{red}

 ██████╗ ████████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
 ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
{reset}""")
    print(f"{green}Coded By Furkan Deniz - @MR0Wido \n \n{reset}")
def main():
    banner()
    args = parser_arguments()
    if args.subdomain_scan:
        subdomain_scan()

    if args.crawler_scan:
        crawler_scan()
    
    if args.dirsearch_scan:
        dirsearch_scan()
    
    if args.filter_list:
        filter_subs_scan()
    
    if args.basic_scan:
        basic_info_scan()
    
    if args.get_screenshot:
        get_screenshot()

if __name__ == "__main__":
    main()
