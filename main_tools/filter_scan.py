from main_tools.common_libs import *
from main_tools.html_output import html_output

def parser_arguments():
    parser = argparse.ArgumentParser(description='Filter subdomains')
    parser.add_argument('-fl', '--filter_list', help='Domain,URL lists for filter', default=None, required=False)
    parser.add_argument('-sc', '--status_codes', type=str, nargs='?', help='Status codes for filter -sc 200,404,500', default=None, required=False)
    parser.add_argument('-p', '--ports', type=str, nargs='?', help='Ports for filter -p 80,443,8080', default=None, required=False)
    parser.add_argument('-clr','--clear_protocol_status_code', help='Clear protocols and status codes', action='store_true', required=False)    
    return parser.parse_args()


def create_directory_from_url(filter_list):
    if '/' in filter_list:
        apart = filter_list.split('/')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name
    else:
        apart = filter_list.split('_')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name

def filter_subs_scan():
    args = parser_arguments()
    filter_list = args.filter_list
    status_codes = args.status_codes
    status_codes_str = ",".join(map(str, status_codes if isinstance(status_codes, (list, tuple)) else [status_codes]))
    ports= args.ports
    ports_str = ",".join(map(str, ports if isinstance(ports, (list, tuple)) else [ports]))
    filtered_subdomains = set()
    output_kind = 'filter_scan'
    directory = create_directory_from_url(filter_list)
    scan_info = 'Filtered subdomains: '

    if '/' in filter_list:
        apart = filter_list.split('/')
        output_filename = apart[0]
        filtered_file = filter_list.replace('.txt', '_filtered.txt')
        filter_temp_file = filter_list.replace('.txt', '_filter_temp.txt')
    
    else:
        apart = filter_list.split('_')
        output_filename = apart[0]
        filtered_file = os.path.join(directory, filter_list.replace('.txt', '_filtered.txt'))
        filter_temp_file = filter_list.replace('.txt', '_filter_temp.txt')

    with open(filter_temp_file, 'w') as f:
        pass

    if filter_list and status_codes is None and ports is None:
        try:
            filter_command_sc = f'httpx -l {filter_list} -p 443,8443,8080,80 -status-code -nc -o {filter_temp_file}'
            filter_out = subprocess.Popen(filter_command_sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with tqdm(desc=colorama.Fore.BLUE + "Filtering: ", unit=colorama.Fore.BLUE + " Domains") as pbar:
                result_lines = 0  
                while True:
                    output = filter_out.stdout.readline()
                    if output == '' and filter_out.poll() is not None:
                        break
                    if output:
                        pbar.update(1)  
                        result_lines += 1  
                        
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"Error: {e}")
    
    elif filter_list and ports and status_codes is None:
        try:
            filter_command_sc = f'httpx -l {filter_list} -p {ports_str} -status-code -nc -o {filter_temp_file}'
            filter_out = subprocess.Popen(filter_command_sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with tqdm(desc=colorama.Fore.BLUE + "Filtering: ", unit=colorama.Fore.BLUE + " Domains") as pbar:
                result_lines = 0  
                while True:
                    output = filter_out.stdout.readline()
                    if output == '' and filter_out.poll() is not None:
                        break
                    if output:
                        pbar.update(1)  
                        result_lines += 1  
                        
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"Error: {e}")

    elif filter_list and status_codes and ports is None:
        try:
            filter_command_sc = f'httpx -l {filter_list} -status-code -mc {status_codes_str} -nc -o {filter_temp_file}'
            filter_out = subprocess.Popen(filter_command_sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with tqdm(desc=colorama.Fore.BLUE + "Filtering: ", unit=colorama.Fore.BLUE + " Domains") as pbar:
                result_lines = 0  
                while True:
                    output = filter_out.stdout.readline()
                    if output == '' and filter_out.poll() is not None:
                        break
                    if output:
                        pbar.update(1)  
                        result_lines += 1  
                        
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"Error: {e}")

    elif filter_list and status_codes and ports:
        try:
            filter_command_sc = f'httpx -l {filter_list} -p {ports_str} -status-code -mc {status_codes_str} -nc -o {filter_temp_file}'
            filter_out = subprocess.Popen(filter_command_sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with tqdm(desc=colorama.Fore.BLUE + "Filtering: ", unit=colorama.Fore.BLUE + " Domains") as pbar:
                result_lines = 0  
                while True:
                    output = filter_out.stdout.readline()
                    if output == '' and filter_out.poll() is not None:
                        break
                    if output:
                        pbar.update(1)  
                        result_lines += 1  
                        
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"Error: {e}")

    if args.clear_protocol_status_code:
        sed_command = f"sed -E 's/^https:\\/\\///; s/^http:\\/\\///; s/\\[.*\\]//g; s/:[0-9]+//g; s/[[:space:]]*$//' {filter_temp_file} | sort -u"
        sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = sed_out.communicate()

        filtered_subdomains= set(output.splitlines())

        with open(filtered_file, 'w') as f:
            f.write('\n'.join(filtered_subdomains))
        
        html_output(output_filename, filtered_file, scan_info, output_kind)

        subprocess.run(['rm', filter_temp_file], check=True)
        print(colorama.Fore.GREEN + f"Filtred: " + blue + directory, f"{result_lines}" + green + " domains are saved in " + blue + f"{filtered_file}")

    elif not args.clear_protocol_status_code:
        with open(filter_temp_file, 'r') as f:
            filtered_subdomains = set(f.read().splitlines())
        
        with open(filtered_file, 'w') as f:
            f.write('\n'.join(filtered_subdomains))
        
        html_output(output_filename, filtered_file, scan_info, output_kind)
        
        subprocess.run(['rm', filter_temp_file], check=True)
        print(colorama.Fore.GREEN + f"Filtred: " + blue + directory, f"{result_lines}" + green + " domains are saved in " + blue + f"{filtered_file}")
        
if __name__ == "__main__":
    filter_subs_scan()
