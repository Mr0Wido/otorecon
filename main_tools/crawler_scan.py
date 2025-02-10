from main_tools.common_libs import *
from main_tools.html_output import html_output
from concurrent.futures import ThreadPoolExecutor, as_completed

def parser_arguments():
    parser = argparse.ArgumentParser(description='Crawler tools')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-cs', '--crawler_scan', help='Specify crawler tools to run or use "all"', nargs='*', choices = ['crawler' , 'waymac', 'waybackurl', 'archive','gau', 'getjs', 'katana', 'cariddi', 'hakrawler', 'golinkfinder','all'], default=None)
    parser.add_argument('-cl', '--crawler_list', help='Crawler list for the crawler scan', default=None, required=False)
    parser.add_argument('-cp', '--crawler_param', help='Crawler result parameter', action='store_true', required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

def split_file(file_path, lines_per_file=1000000):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    file_count = 0
    for i in range(0, len(lines), lines_per_file):
        with open(f"{file_path}_part{file_count}", 'w') as part_file:
            part_file.writelines(lines[i:i+lines_per_file])
        file_count += 1
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

def run_tool(tool, crawler_list, crawler_domain, perform_crawler_scan,   urls_output_temp_file):
    try:
        if  tool == 'crawler':
            if crawler_list:
                crawler_command = f'python3 main_tools/tools/crawler.py -l {crawler_list} | sort -u'
            elif crawler_domain:
                crawler_command = f'python3 main_tools/tools/crawler.py -d {crawler_domain}  | sort -u'
            with open(urls_output_temp_file, 'a') as f:
                crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output = crawler_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'waymac':
            if crawler_list:
                waymac_command = f'python3 main_tools/tools/waybackMachine.py -l {crawler_list} | sort -u'
            elif crawler_domain:
                waymac_command = f'python3 main_tools/tools/waybackMachine.py -d {crawler_domain}  | sort -u'
            with open(urls_output_temp_file, 'a') as f:
                waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = waymac_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'archive':
            if crawler_list:
                archive_command = f'python3 main_tools/tools/archive.py -l {crawler_list} | sort -u'   
            elif crawler_domain:
                archive_command = f'python3 main_tools/tools/archive.py -d {crawler_domain}  | sort -u'   
            with open(urls_output_temp_file, 'a') as f:
                archive_out = subprocess.Popen(archive_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = archive_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")           
            
        elif tool == 'waybackurl':
            if crawler_list:        
                waybackurl_command = f'cat {crawler_list} | waybackurls | sort -u'      
            elif crawler_domain:
                waybackurl_command = f'waybackurls {crawler_domain}  | sort -u'      
            with open(urls_output_temp_file, 'a') as f:
                waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = waybackurl_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            

        elif tool == 'gau':
            if crawler_list:
                gau_command = f'cat {crawler_list} | gau | sort -u'      
            elif crawler_domain:
                gau_command = f'gau {crawler_domain}  | sort -u'  
            with open(urls_output_temp_file, 'a') as f:    
                gau_out = subprocess.Popen(gau_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = gau_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            
        elif tool == 'getjs':
            with open(getJS_temp_file, 'w') as f:
                pass
            sed_command= f"sed 's#^#https://#' {crawler_list} | sort -u"
            with open(getJS_temp_file, 'a') as f:
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                sed_output, error = sed_out.communicate()

            if crawler_list:
                with open(getJS_temp_file, 'r') as f:
                    urls = set(f.read().splitlines())
                    for url in urls: 
                        getJS_command = f'getjs --url {url}'
            elif crawler_domain:
                getJS_command = f'getjs --url {crawler_domain}  | sort -u'
            with open(urls_output_temp_file, 'a') as f:
                getJS_out = subprocess.Popen(getJS_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = getJS_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            subprocess.run(['rm', '-f', getJS_temp_file], check=True)

        elif tool == 'katana':
            if crawler_list:
                katana_command = f'katana -list {crawler_list} -nc -silent | sort -u'   
            elif crawler_domain:
                katana_command = f'katana -u {crawler_domain}  -nc -silent | sort -u'   
            with open(urls_output_temp_file, 'a') as f:
                katana_out = subprocess.Popen(katana_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = katana_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")

        elif tool == 'cariddi':
            with open(cariddi_temp_file, 'w') as f:
                pass
            sed_command= f"sed 's#^#https://#' {crawler_list} | sort -u"
            with open(cariddi_temp_file, 'a') as f:
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                sed_output, error = sed_out.communicate()
            if crawler_list:
                cariddi_command = f'cat {cariddi_temp_file} | cariddi -plain'   
            elif crawler_domain:
                cariddi_command = f'echo {crawler_domain} | cariddi -plain | sort -u'
            with open(urls_output_temp_file, 'a') as f:   
                cariddi_out = subprocess.Popen(cariddi_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = cariddi_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            subprocess.run(['rm', '-f', cariddi_temp_file], check=True)
        
        elif tool == 'hakrawler':
            with open(hakrawler_temp_file, 'w') as f:
                pass
            sed_command= f"sed 's#^#https://#' {crawler_list} | sort -u"
            with open(hakrawler_temp_file, 'a') as f:
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                sed_output, error = sed_out.communicate()
            if crawler_list:
                hakrawler_command = f'cat {hakrawler_temp_file} | hakrawler -subs'
            elif crawler_domain:
                hakrawler_command = f'echo https://{crawler_domain} |  hakrawler -subs | sort -u'
            with open(urls_output_temp_file, 'a') as f:   
                hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = hakrawler_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            subprocess.run(['rm', '-f', hakrawler_temp_file], check=True)

        elif tool == 'golinkfinder': 
            with open(golinkfinder_temp_file, 'w') as f:
                pass
            if crawler_list:
                with open(crawler_list, 'r') as f:
                    urls = set(f.read().splitlines())
                    for url in urls: 
                        golinkfinder_command = f'golinkfinder -d {url}'
            elif crawler_domain:
                golinkfinder_command = f'golinkfinder -d {crawler_domain}  | sort -u'
            with open(urls_output_temp_file, 'a') as f:
                golinkfinder_out = subprocess.Popen(golinkfinder_command, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True)
                output, error = golinkfinder_out.communicate()
            print (blue + f"{tool}" + green + " completed successfully.")
            subprocess.run(['rm', '-f', golinkfinder_temp_file], check=True)
            
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

def process_file_part(file_part, urls_output_file, urls_output_file_js):
    try:
        first_sed_command = f"sed -e '/\\.js$/d' {file_part} | sort -u"
        first_sed_command_out = subprocess.Popen(first_sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = first_sed_command_out.communicate()
        nonjs_urls = set(output.splitlines())
        with open(urls_output_file, 'w') as f:
            f.write('\n'.join(nonjs_urls))
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"sed returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
    
    try:
        second_sed_command = f"sed -E '/js/!d' {file_part} | sort -u"
        second_sed_command_out = subprocess.Popen(second_sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = second_sed_command_out.communicate()
        withjs_urls = set(output.splitlines())
        with open(urls_output_file_js, 'w') as f:
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
        scan_info = 'Crawler Scan Result (Not include .js files): '
        scan_info_js = 'Crawler Scan Result (Only .js files): '
    
    elif crawler_list and not '/' in crawler_list:
        apart = crawler_list.split('_')
        output_filenmae = apart[0]
        urls_output_file = os.path.join(directory, f'{output_filenmae}_urls.txt')
        urls_output_file_js = os.path.join(directory, f'{output_filenmae}_jsurls.txt')
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        scan_info = 'Crawler Scan Result (Not include .js files): '
        scan_info_js = 'Crawler Scan Result (Only .js files): '

    elif crawler_domain:
        urls_output_file_js = os.path.join(directory, f'{crawler_domain}_jsurls.txt')
        urls_output_file = os.path.join(directory, f'{crawler_domain}_urls.txt')
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        output_filenmae = f'{crawler_domain}'
        scan_info = 'Crawler Scan (Not include .js files): '
        scan_info_js = 'Crawler Scan Result (Only .js files): '
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

    if crawler_list:
        print(colorama.Fore.CYAN + f"Running tools on {crawler_list}.....")
    elif crawler_domain:
        print(colorama.Fore.CYAN + f"Running tools on {crawler_domain}.....")

    max_threads = min(10, len(crawler_tools))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for tool in crawler_tools:
            if tool not in perform_crawler_scan and 'all' not in args.crawler_scan:
                continue
            futures.append(executor.submit(run_tool, tool, crawler_list, crawler_domain, perform_crawler_scan, urls_output_temp_file))

        for future in as_completed(futures):
            future.result()

    with open(urls_output_temp_file, 'r') as f:
        crawler_temp_out = set(f.read().splitlines())
    
    print(colorama.Fore.GREEN + f"Total " + blue + f"{len(crawler_temp_out)}" + green + " URLs found. Successfully printed to the " + blue + f'{urls_output_temp_file}' + green + " file.")
    
    print(colorama.Fore.CYAN + f"Parsing .js URLs on {urls_output_temp_file}")
    

    split_file(urls_output_temp_file)
    part_files = [f for f in os.listdir() if f.startswith(urls_output_temp_file)]

    with ThreadPoolExecutor(max_workers=len(part_files)) as executor:
        futures = [executor.submit(process_file_part, part_file, urls_output_file, urls_output_file_js) for part_file in part_files]
        for future in as_completed(futures):
            future.result()

    for part_file in part_files:
        subprocess.run(['rm', '-f', part_file], check=True)

    print(green + f"Parsed URLs Successfully printed to the " + blue + f'{urls_output_file}' + green + " and " + blue + f'{urls_output_file_js}' + green + " file.")

    html_output(output_filenmae, urls_output_file, scan_info, output_kind)
    html_output(output_filenmae, urls_output_file_js, scan_info_js, output_kind)


    if args.crawler_param:
        try:
            scan_info_param = 'Sending URLs to paramspider to get parameters'
            print(colorama.Fore.CYAN + f"Extracting parameters from {urls_output_file}...")
            param_command = f'python3 main_tools/tools/clean_urls.py -u {urls_output_file} -o {param_output_file}'
            param_out = subprocess.Popen(param_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = param_out.communicate()

            print(colorama.Fore.GREEN + f'Extracted parameters Successfully printed to the ' + blue + f'{param_output_file}')
            html_output(output_filenmae, param_output_file, scan_info_param, output_kind)
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"paramspider returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

        try:
            scan_info_endpoints = 'Sending URLs to endpoint_finder to get endpoints and info from .js files'
            kind = 'endpoint_finder'
            print(colorama.Fore.CYAN + f"Extracting endpoints from {urls_output_file_js}...")
            with open(urls_output_file_js, 'r') as f:
                urls = set(f.read().splitlines())
                for url in urls:
                    list_command = f"python3 main_tools/tools/endpoint_finder.py -u {url} -o {endpointjs_output_file}"
                    list_command_out = subprocess.Popen(list_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = list_command_out.communicate()
                
            print(colorama.Fore.GREEN + f'Extracted endpoints Successfully printed to the ' + blue + f'{endpointjs_output_file}')
            html_output(output_filenmae, endpointjs_output_file, scan_info_endpoints, kind)
        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"endpoint_finder returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
            
if __name__ == "__main__":
    crawler_scan()
