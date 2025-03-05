from main_tools.common_libs import *
from main_tools.html_output import html_output
from concurrent.futures import ThreadPoolExecutor, as_completed

dirsearch_tools = ['rd1000', 'raft', 'dirm2_3', 'dirsearch']  # Tanımlanmamış değişken

def parser_arguments():
    parser = argparse.ArgumentParser(description='Directory Search')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)    
    parser.add_argument('-ds', '--dirsearch_scan', help='Directory Search', nargs='*', choices=dirsearch_tools + ['all'], default=None)
    parser.add_argument('-dl', '--dirsearch_list', help='Subdomain list for the directory scan', default=None, required=False)
    return parser.parse_args()  

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))
    
def create_directory_from_url(dirsearch_list, domain_name):
    if dirsearch_list and '/' in dirsearch_list:
        apart = dirsearch_list.split('/')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name
    elif dirsearch_list and not '/' in dirsearch_list:
        apart = dirsearch_list.split('_')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
    elif domain_name:
        if not os.path.exists(domain_name):
            os.mkdir(domain_name)
        return domain_name
    else:
        return None

def run_gobuster(tool, dirsearch_list, dirsearch_domain, directories_output_file):
    try:
        if dirsearch_list:
            dir_filter_temp_file = 'dir_filter_temp_file.txt'
            probed_domains_file = 'probed_domains_file.txt'
            filter_command = f"httpx -l {dirsearch_list} -title -sc -location -p 80,443,8000,8080,8443 -td -cl -probe -nc -o {dir_filter_temp_file}"
            filter_out = subprocess.Popen(filter_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = filter_out.communicate()
            
            sed_command = f"cat {dir_filter_temp_file} | grep -v \"FAILED\" | awk '{{print $1}}' >> {probed_domains_file}"
            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = sed_out.communicate()
            
            dirsearch_command = f"xargs -a {probed_domains_file} -I@ sh -c 'gobuster dir -u \"@\" --no-color -f -q -k -e --no-error -w main_tools/wordlists/dirsearch_wordlists/{tool}.txt' | sed 's/\x1B\[[0-9;]*[mK]//g' | tee -a {directories_output_file}"
            dirsearch_out = subprocess.Popen(dirsearch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = dirsearch_out.communicate()

            dirsearch= set(output.splitlines())
            write_to_file(directories_output_file, dirsearch)
        
        elif dirsearch_domain:
            dirsearch_command = f"gobuster dir -u https://{dirsearch_domain} -w main_tools/wordlists/dirsearch_wordlists/{tool}.txt -f -q -k -e --hide-length --no-color --no-error -o {directories_output_file}"
            dirsearch_out = subprocess.Popen(dirsearch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = dirsearch_out.communicate()

            dirsearch= set(output.splitlines())
            write_to_file(directories_output_file, dirsearch)

        subprocess.run(['rm', '-f', dir_filter_temp_file], check=True)
        subprocess.run(['rm', '-f', probed_domains_file], check=True)
        
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
        return

def dirsearch_scan():
    args = parser_arguments()
    dirsearch_list = args.dirsearch_list
    dirsearch_domain = args.domain_name
    dirsearch_scan = args.dirsearch_scan
    output_kind = 'dirsearch_scan'
    directory = create_directory_from_url(dirsearch_list, dirsearch_domain)    

    if dirsearch_list and '/' in dirsearch_list:
        apart = dirsearch_list.split('/')
        output_filename = apart[0]
        directories_output_file = os.path.join(directory, f'{output_filename}_dirs.txt')
        scan_info = 'Directory Bruteforce: '
    elif dirsearch_list and not '/' in dirsearch_list:
        apart = dirsearch_list.split('_')
        output_filename = apart[0]
        directories_output_file = os.path.join(directory, f'{output_filename}_dirs.txt')
        scan_info = 'Directory Bruteforce: '
    elif dirsearch_domain:
        directories_output_file = os.path.join(directory, f'{dirsearch_domain}_dirs.txt')
        output_filename = f'{dirsearch_domain}'
        scan_info = 'Directory Bruteforce: '
    else:
        print(colorama.Fore.RED + 'The following arguments are required: --dl/--dirsearch_list')
        print(colorama.Fore.RED + 'The following arguments are required: --d/--domain_name')
        sys.exit(1)
    

    with open(directories_output_file, 'w') as f:
        pass

    if dirsearch_list:
        print(colorama.Fore.CYAN + f" [*] Gobuster running on " + colorama.Fore.GREEN + f"{dirsearch_list}" )
    elif dirsearch_domain:
        print(colorama.Fore.CYAN + f" [*] Gobuster running on " + colorama.Fore.GREEN + f"{dirsearch_domain}" )
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for tool in dirsearch_tools:
            if tool not in args.dirsearch_scan and 'all' not in args.dirsearch_scan:
                continue
            futures.append(executor.submit(run_gobuster, tool, dirsearch_list, dirsearch_domain, directories_output_file))

        for future in as_completed(futures):
            future.result()
    

    print(colorama.Fore.GREEN + f" [*] Directory Search completed. Successfully printed to the " + colorama.Fore.BLUE + f"{directories_output_file}" + colorama.Fore.GREEN + " has been created.")
    html_output(output_filename, directories_output_file, scan_info, output_kind)

if __name__ == "__main__":
    dirsearch_scan()