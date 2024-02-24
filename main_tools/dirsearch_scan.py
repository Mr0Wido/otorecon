from main_tools.common_libs import *
from main_tools.html_output import html_output

def parser_arguments():
    parser = argparse.ArgumentParser(description='Directory Search')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)    
    parser.add_argument('-ds', '--dirsearch_scan', help='Directory Search', nargs='*', choices = ['rd1000', 'raft', 'dirm2_3', 'dirsearch', 'all'], default=None)
    parser.add_argument('-dl', '--dirsearch_list', help='Subdomain list for the directory scan', default=None, required=False)
    return parser.parse_args()  

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))
    

def dirsearch_scan():
    args = parser_arguments()
    dirsearch_list = args.dirsearch_list
    dirsearch_domain = args.domain_name
    dirsearch_temp = set()
    dirsearch_temp_out = set()
    dirsearch_result = set()
    output_kind = 'dirsearch_scan'
    

    if dirsearch_list:
        directories_output_file = dirsearch_list.replace('.txt', '_dirs.txt')
        apart = dirsearch_list.split('_')
        output_filenmae = apart[0]
        scan_info = 'Directory Bruteforce: '
    elif dirsearch_domain:
        directories_output_file = f'{dirsearch_domain}_dirs.txt'
        output_filenmae = f'{dirsearch_domain}'
        scan_info = 'Directory Bruteforce: '
    else:
        print(colorama.Fore.RED + 'The following arguments are required: --dl/--dirsearch_list')
        print(colorama.Fore.RED + 'The following arguments are required: --d/--domain_name')
        sys.exit(1)
    

    with open(directories_output_file, 'w') as f:
        pass

    for tool in dirsearch_tools:
        if dirsearch_list:
            print(colorama.Fore.CYAN + f"Running {tool} on {dirsearch_list}")
        elif dirsearch_domain:
            print(colorama.Fore.CYAN + f"Running {tool} on {dirsearch_domain}")
        if tool not in args.dirsearch_scan and 'all' not in args.dirsearch_scan:
            continue
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
            subprocess.run(['rm', f'{tool}_temp.txt'], check=True)
            
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
            continue

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