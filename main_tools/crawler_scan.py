from main_tools.common_libs import *
from main_tools.html_output import html_output
from concurrent.futures import ThreadPoolExecutor, as_completed

def parser_arguments():
    parser = argparse.ArgumentParser(description='Crawler tools')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-cs', '--crawler_scan', help='Specify crawler tools to run or use "all"', nargs='*', choices = ['crawler' , 'waymac', 'waybackurl', 'gau', 'katana', 'getjs', 'hakrawler', 'all'], default=None)
    parser.add_argument('-cl', '--crawler_list', help='Crawler list for the crawler scan', default=None, required=False)
    parser.add_argument('-cp', '--crawler_param', help='Crawler result parameter', action='store_true', required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))


def create_directory_from_url(crawler_list, crawler_domain):
    if crawler_list and '/' in crawler_list:
        apart = crawler_list.split('/')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name
    elif crawler_list and not '/' in crawler_list:
        apart = crawler_list.split('_')
        directory_name = apart[0]
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name 
    elif crawler_domain:
        directory_name = crawler_domain
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return directory_name
    else:
        return None

def run_tool(tool, crawler_list, crawler_domain, urls_output_temp_file, perform_crawler_scan, urls_output_file_js):
    try:
        if  tool == 'crawler':
            if crawler_list:
                crawler_command = f'python3 main_tools/tools/crawler.py -l {crawler_list} -o {crawler_temp_file}'
                crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = crawler_out.communicate()
            
            elif crawler_domain:
                crawler_command = f'python3 main_tools/tools/crawler.py -d {crawler_domain} -o {crawler_temp_file}'
                crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = crawler_out.communicate()
            
            uro_command = f"cat {crawler_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'waymac':
            if crawler_list:
                waymac_command = f'python3 main_tools/tools/waybackMachine.py -l {crawler_list} -o {waymac_temp_file}'
                waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = waymac_out.communicate()
            elif crawler_domain:
                waymac_command = f'python3 main_tools/tools/waybackMachine.py -d {crawler_domain} -o {waymac_temp_file}'
                waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = waymac_out.communicate()
            
            uro_command = f"cat {waymac_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()
            set(output.splitlines())
            print (green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'waybackurl':
            if crawler_list:        
                waybackurl_command = f'cat {crawler_list} | waybackurls >> {waybackurl_temp_file}'   
                waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = waybackurl_out.communicate()   
            elif crawler_domain:
                waybackurl_command = f'waybackurls {crawler_domain} >> {waybackurl_temp_file}'
                waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = waybackurl_out.communicate()

            uro_command = f"cat {waybackurl_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()      
            print (green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")
            

        elif tool == 'gau':
            if crawler_list:
                gau_command = f'cat {crawler_list} | gau --subs >> {gau_temp_file}'      
                gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = gau_out.communicate()
            elif crawler_domain:
                gau_command = f'gau --subs {crawler_domain} >> {gau_temp_file}'
                gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = gau_out.communicate()

            uro_command = f"cat {gau_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()  
            print (green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")
            
        elif tool == 'katana':
            if crawler_list:
                katana_command = f'katana -list {crawler_list} -nc -silent -o {katana_temp_file}'
                katana_out = subprocess.Popen(katana_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = katana_out.communicate()   
            elif crawler_domain:
                katana_command = f'katana -u {crawler_domain}  -nc -silent -o {katana_temp_file}'
                katana_out = subprocess.Popen(katana_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = katana_out.communicate()

            uro_command = f"cat {katana_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()   
            print (green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'hakrawler':
            if crawler_list:
                hakrawler_command = f'cat {crawler_list} | httpx | hakrawler -subs -u >> {hakrawler_temp_file}'
                hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = hakrawler_out.communicate()
            elif crawler_domain:
                hakrawler_command = f'echo https://{crawler_domain} |  hakrawler -subs -u >> {hakrawler_temp_file}'
                hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output = hakrawler_out.communicate()

            uro_command = f"cat {hakrawler_temp_file} | uro >> {uro_log_file}"
            uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, error = uro_out.communicate()
            print (green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")

            
        elif tool == 'getjs':
            with open(crawler_list, 'r') as file:
                urls = [f"https://{line.strip()}" for line in file.readlines() if line.strip()]

            with open(getJS_temp_file, 'a') as f:
                for url in urls:
                    getjs_command = f'getjs --url {url}'
                    print(getjs_command)
                    getjs_out = subprocess.Popen(getjs_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                    output, error = getjs_out.communicate()
                    output_urls = [f"{url}{line.strip()}" for line in output.splitlines() if line.strip()]
                    f.write('\n'.join(output_urls) + '\n')

            
            with open(getJS_temp_file, 'r') as f:
                getjs_urls = set(f.read().splitlines())

            with open(urls_output_file_js, 'w') as out_file:
                out_file.write("\n".join(getjs_urls))
                    
            print(green + "    [+] " + blue + f"{tool}" + green + " completed successfully.")
        
        uro_command = f"cat {uro_log_file} | uro >> {urls_output_temp_file}"
        uro_out = subprocess.Popen(uro_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = uro_out.communicate()

    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

def extract_js(urls_output_file_js, urls_output_temp_file):
    try:
        second_sed_command = f"sed -E '/js/!d' {urls_output_temp_file}"
        second_sed_command_out = subprocess.Popen(second_sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = second_sed_command_out.communicate()
        withjs_urls = set(output.splitlines())
        with open(urls_output_file_js, 'a') as f:
            f.write('\n'.join(withjs_urls))
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"sed returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
    

def crawler_scan():
    args = parser_arguments()
    crawler_list = args.crawler_list
    perform_crawler_scan = args.crawler_scan
    crawler_domain = args.domain_name
    crawler_temp_out = set()
    nonjs_urls = set()
    withjs_urls = set()
    output_kind = 'crawler_scan'
    urls_output_temp_file = 'urls_temp_output.txt'

    directory = create_directory_from_url(crawler_list, crawler_domain)

    if crawler_list and '/' in crawler_list:
        apart = crawler_list.split('/')
        output_filenmae = apart[0]
        urls_output_file = os.path.join(directory, f'{output_filenmae}_urls.txt')
        urls_output_file_js = os.path.join(directory, f'{output_filenmae}_jsurls.txt')
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        scan_info = 'Crawler scan '
        scan_info_js = 'Crawler scan (only .js files) '
    
    elif crawler_list and not '/' in crawler_list:
        apart = crawler_list.split('_')
        output_filenmae = apart[0]
        urls_output_file = os.path.join(directory, f'{output_filenmae}_urls.txt')
        urls_output_file_js = os.path.join(directory, f'{output_filenmae}_jsurls.txt')
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        scan_info = 'Crawler Scan '
        scan_info_js = 'Crawler Scan (only .js files)'

    elif crawler_domain:
        urls_output_file_js = os.path.join(directory, f'{crawler_domain}_jsurls.txt')
        urls_output_file = os.path.join(directory, f'{crawler_domain}_urls.txt')
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        output_filenmae = f'{crawler_domain}'
        scan_info = 'Crawler scan '
        scan_info_js = 'Crawler scan (only .js files): '
    else:
        print(colorama.Fore.RED + 'The following arguments are required: -cl/--crawler_list')
        print(colorama.Fore.RED + 'The following arguments are required: -d/--domain_name')
        sys.exit(1)

    with open(urls_output_temp_file, 'w') as f:
        pass
    with open(urls_output_file, 'w') as f:
        pass
    with open(urls_output_file_js, 'w') as f:
        pass
    with open(uro_log_file, 'w') as f:
        pass

    if crawler_list:
        print(colorama.Fore.CYAN + f" [*] Running tools on " + green + f"{crawler_list}.....")
    elif crawler_domain:
        print(colorama.Fore.CYAN + f" [*] Running tools on " + green + f"{crawler_domain}.....")

    max_threads = min(10, len(crawler_tools))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for tool in crawler_tools:
            if tool not in perform_crawler_scan and 'all' not in args.crawler_scan:
                continue
            futures.append(executor.submit(run_tool, tool, crawler_list, crawler_domain, perform_crawler_scan, urls_output_temp_file, urls_output_file_js))

        for future in as_completed(futures):
            future.result()

    with open(urls_output_temp_file, 'r') as f:
        crawler_temp_out = set(f.read().splitlines())

    print( magenta + f" [+] Total " + blue + f"{len(crawler_temp_out)}" + magenta + " URLs found. Successfully printed to the " + blue + f'{urls_output_temp_file}' + magenta + " file.")
    
    print(colorama.Fore.CYAN + f" [*] Extracting JavaScript Sources from URLs {urls_output_temp_file}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        futures.append(executor.submit(extract_js, urls_output_file_js, urls_output_temp_file))

        for future in as_completed(futures):
            future.result()

    print(magenta + f" [+] Parsed URLs Successfully printed to the " + blue + f'{urls_output_file}' + green + " and " + blue + f'{urls_output_file_js}' + green + " file.")

    if args.crawler_param:
        try:
            scan_info_param = 'Sending URLs to paramspider to get parameters'
            print(colorama.Fore.CYAN + f" [*] Extracting parameters from {urls_output_file}...")
            param_command = f'python3 main_tools/tools/clean_urls.py -u {urls_output_file} -o {param_output_file}'
            param_out = subprocess.Popen(param_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = param_out.communicate()

            print(magenta + f' [+] Extracted parameters Successfully printed to the ' + blue + f'{param_output_file}')
            html_output(output_filenmae, param_output_file, scan_info_param, output_kind)
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"paramspider returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

        try:
            scan_info_endpoints = 'Sending URLs to endpoint_finder to get endpoints and info from .js files'
            kind = 'endpoint_finder'
            print(colorama.Fore.CYAN + f" [*] Extracting endpoints from {urls_output_file_js}...")
            with open(urls_output_file_js, 'r') as f:
                urls = set(f.read().splitlines())
                for url in urls:
                    list_command = f"python3 main_tools/tools/endpoint_finder.py -u {url} -o {endpointjs_output_file}"
                    list_command_out = subprocess.Popen(list_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = list_command_out.communicate()
                
            print(magenta + f' [+] Extracted endpoints Successfully printed to the ' + blue + f'{endpointjs_output_file}')
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"endpoint_finder returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
            
            html_output(output_filenmae, urls_output_file, scan_info, output_kind)
            html_output(output_filenmae, urls_output_file_js, scan_info_js, output_kind)
            html_output(output_filenmae, endpointjs_output_file, scan_info_endpoints, kind)
if __name__ == "__main__":
    crawler_scan()
