from main_tools.common_libs import *
from main_tools.html_output import html_output
from concurrent.futures import ThreadPoolExecutor, as_completed

def parser_arguments():
    parser = argparse.ArgumentParser(description='Directory Search')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)    
    parser.add_argument('-ds', '--dirsearch_scan', help='Directory Search', nargs='*', choices = ['rd1000', 'raft', 'dirm2_3', 'dirsearch', 'all'], default=None)
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

def run_gobuster(tool, dirsearch_list, dirsearch_domain, dirsearch_temp, dirsearch_temp_out):
        try:
            with open (f'{tool}_temp.txt', 'w') as f:
                pass
            
            if dirsearch_list:
                with open(dirsearch_list, 'r') as f:
                    subdomains = set(f.read().splitlines())

                for subdomain in subdomains:
                    command = f'gobuster dir -u https://{subdomain} -w main_tools/wordlists/dirsearch_wordlists/{tool}.txt --no-color --no-error -o {tool}_temp.txt'
                    command_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = command_out.communicate()

                    with open(f'{tool}_temp.txt', 'r') as f:
                        temp_result = f.readlines()

                    with open(f'{tool}.txt', 'w') as f:
                        for line in temp_result:
                            f.write(f'{subdomain}: {line}')
                    
                    with open(f'{tool}.txt', 'r') as f:
                        temp_out = sorted(f.read().splitlines())
                    
                    dirsearch_temp_out.update(temp_out)

            elif dirsearch_domain:
                command = f'gobuster dir -u https://{dirsearch_domain} -w main_tools/wordlists/dirsearch_wordlists/{tool}.txt --no-color --no-error -o {tool}_temp.txt'
                command_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = command_out.communicate()

                with open(f'{tool}_temp.txt', 'r') as f:
                    temp_result = f.readlines()

                with open(f'{tool}.txt', 'w') as f:
                    for line in temp_result:
                        f.write(f'{dirsearch_domain}: {line}')

                with open (f'{tool}.txt', 'r') as f:
                    temp_out = f.read().splitlines()

                dirsearch_temp_out.update(temp_out)
            
            dirsearch_temp.update(dirsearch_temp_out)
            write_to_file(f'{tool}.txt', dirsearch_temp_out)
            subprocess.run(['rm', '-f', f'{tool}_temp.txt'], check=True)
            
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
            return

def dirsearch_scan():
    args = parser_arguments()
    dirsearch_list = args.dirsearch_list
    dirsearch_domain = args.domain_name
    dirsearch_temp = set()
    dirsearch_temp_out = set()
    dirsearch_result = set()
    output_kind = 'dirsearch_scan'
    directory = create_directory_from_url(dirsearch_list, dirsearch_domain)    

    if dirsearch_list:
        directories_output_file = dirsearch_list.replace('.txt', '_dirs.txt')
        apart = dirsearch_list.split('_')
        output_filenmae = apart[0]
        scan_info = 'Directory Bruteforce: '
    elif dirsearch_domain:
        directories_output_file = os.path.join(directory, f'{dirsearch_domain}_dirs.txt')
        output_filenmae = f'{dirsearch_domain}'
        scan_info = 'Directory Bruteforce: '
    else:
        print(colorama.Fore.RED + 'The following arguments are required: --dl/--dirsearch_list')
        print(colorama.Fore.RED + 'The following arguments are required: --d/--domain_name')
        sys.exit(1)
    

    with open(directories_output_file, 'w') as f:
        pass

    if dirsearch_list:
        print(colorama.Fore.CYAN + f"Running tools on " + green + f"{dirsearch_list}" )
    elif dirsearch_domain:
        print(colorama.Fore.CYAN + f"Running tools on " + green + f"{dirsearch_domain}" )
        
    max_threads = min(10, len(dirsearch_list))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for tool in dirsearch_tools:
            if tool not in args.dirsearch_scan and 'all' not in args.dirsearch_scan:
                continue
            futures.append(executor.submit(run_gobuster, tool, dirsearch_list, dirsearch_domain, dirsearch_temp, dirsearch_temp_out))

        for future in as_completed(futures):
            future.result()

    dirsearch_result.update(dirsearch_temp)        
    with open(directories_output_file, 'w') as f:
        f.write('\n'.join(dirsearch_result))

    for tool in dirsearch_tools:
        file_to_remove = f'{tool}.txt'
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)

    print(colorama.Fore.GREEN + f"Directory Search completed. Successfully printed to the " + blue + f"{directories_output_file}" + green + " has been created")
    html_output(output_filenmae, directories_output_file, scan_info, output_kind)
if __name__ == "__main__":
    dirsearch_scan()