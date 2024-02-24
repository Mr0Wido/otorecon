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

#Baisc_info variables
dnmasscan_temp_file = 'dnmasscan_temp.txt'
whatweb_temp_file = 'whatweb_temp.txt'

# Subdomain_scan variables
amass_temp_file         = 'amass_temp.txt'
sublist3r_temp_file     = 'sublist3r_temp.txt'
shuffledns_temp_file       = 'massdns_output.txt'
dnsgen_temp_file        = 'dnsgen_temp.txt'
remaine_temp_file       = 'remaine.txt'
domain_file             = 'domain.txt'
wfuzz_temp_file         = 'wfuzz_temp.txt'
altdns_temp_file        = 'altdns_temp.txt'

# Crawler_scan variables
crawler_temp_file       = 'crawler_temp.txt'
waymac_temp_file        = 'waymac_temp.txt'
cocrawl_temp_file       = 'cocrawl_temp.txt'
waybackurl_temp_file    = 'waybackurl_temp.txt'
archive_temp_file       = 'archive_temp.txt'
gau_temp_file           = 'gau_temp.txt'
getJS_temp_file         = 'getJS_temp.txt'
getJS_out_file          = 'getJS_out.txt'
katana_temp_file        = 'katana_temp.txt'
cariddi_temp_file       = 'cariddi_temp.txt'
cariddi_out_file        = 'cariddi_out.txt'
hakrawler_temp_file     = 'hakrawler_temp.txt'
hakrawler_out_file      = 'hakrawler_out.txt'
golinkfinder_temp_file  = 'golinkfinder_temp.txt'


# Dirsearch_scan variables
rd1000_temp_file       = 'rd1000_temp.txt'
raft_temp_file         = 'raft_temp.txt'
dirm2_3_temp_file      = 'dirm2_3_temp.txt'
dirsearch_temp_file    = 'dirsearch_temp.txt'

# filter_scan variables
filter_temp_file        = 'filter_temp.txt'

# Tools
basic_info_tools = ['dnmasscan', 'whatweb']
crawler_tools  = ['crawler', 'waymac', 'cocrawl', 'waybackurl', 'archive', 'gau', 'getjs', 'katana', 'cariddi', 'hakrawler', 'golinkfinder']
dirsearch_tools = ['rd1000', 'raft', 'dirm2_3', 'dirsearch']
param_scan_tools = ['paramspider', 'cleanurls']

