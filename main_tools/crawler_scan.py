from main_tools.common_libs import *
from main_tools.html_output import html_output

def parser_arguments():
    parser = argparse.ArgumentParser(description='Crawler tools')
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-cs', '--crawler_scan', help='Specify crawler tools to run or use "all"', nargs='*', choices = ['crawler' , 'waymac', 'cocrawl', 'waybackurl', 'archive','gau', 'getjs', 'katana', 'cariddi', 'hakrawler', 'golinkfinder','all'], default=None)
    parser.add_argument('-cl', '--crawler_list', help='Crawler list for the crawler scan', default=None, required=False)
    parser.add_argument('-cp', '--crawler_param', help='Crawler result parameter', action='store_true', required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

def crawler_scan():
    args = parser_arguments()
    crawler_list = args.crawler_list
    perform_crawler_scan = args.crawler_scan
    crawler_domain = args.domain_name
    crawler_temp = set()
    crawler_temp_out = set()
    nonjs_urls = set()
    withjs_urls = set()
    output_kind = 'crawler_scan'
    urls_output_temp_file = 'urls_output_temp.txt'

    if crawler_list:
        apart = crawler_list.split('_')
        output_filenmae = apart[0]
        urls_output_file = f'{output_filenmae}_urls.txt'
        urls_output_file_js = f'{output_filenmae}_jsurls.txt'
        param_output_file = urls_output_file.replace('.txt', '_param.txt')
        endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
        scan_info = 'Crawler Scan Result (Not include .js files): '
        scan_info_js = 'Crawler Scan Result (Only .js files): '
    elif crawler_domain:
        urls_output_file_js = f'{crawler_domain}_jsurls.txt'
        urls_output_file = f'{crawler_domain}_urls.txt'
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

    for tool in crawler_tools:
        if crawler_list:
            print(colorama.Fore.CYAN + f"Running {tool} on {crawler_list}")
        elif crawler_domain:
            print(colorama.Fore.CYAN + f"Running {tool} on {crawler_domain}")
        if tool not in perform_crawler_scan and 'all' not in args.crawler_scan:
            continue
        try:
            if  tool == 'crawler':
                with open(crawler_temp_file, 'w') as f:
                    pass

                if crawler_list:
                    crawler_command = f'python3 main_tools/tools/crawler.py -l {crawler_list} -o {crawler_temp_file}'
                    crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output = crawler_out.communicate()

                elif crawler_domain:
                    crawler_command = f'python3 main_tools/tools/crawler.py -d {crawler_domain} -o {crawler_temp_file}'
                    crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output = crawler_out.communicate()

                with open(crawler_temp_file, 'r') as f:
                    crawler_result = set(f.read().splitlines())
                    
                crawler_temp.update(crawler_result)
                subprocess.run(['rm', crawler_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(crawler_result)) + green + " subdomains.")

            elif tool == 'waymac':
                with open(waymac_temp_file, 'w') as f:
                    pass

                if crawler_list:
                    waymac_command = f'python3 main_tools/tools/waybackMachine.py -l {crawler_list} -o {waymac_temp_file}'
                    waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = waymac_out.communicate()

                elif crawler_domain:
                    waymac_command = f'python3 main_tools/tools/waybackMachine.py -d {crawler_domain} -o {waymac_temp_file}'
                    waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = waymac_out.communicate()

                with open(waymac_temp_file, 'r') as f:
                    waymac_result = set(f.read().splitlines())

                crawler_temp.update(waymac_result)  
                subprocess.run(['rm', waymac_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(waymac_result)) + green + " subdomains.")

            elif tool == 'cocrawl':
                with open(cocrawl_temp_file, 'w') as f:
                    pass

                if crawler_list:                
                    cocrawl_command = f'python3 main_tools/tools/commoncrawl.py -l {crawler_list} | tee -a {cocrawl_temp_file}'
                    cocrawl_out = subprocess.Popen(cocrawl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = cocrawl_out.communicate()
                    
                elif crawler_domain:
                    cocrawl_command = f'python3 main_tools/tools/commoncrawl.py -d {crawler_domain} | tee -a {cocrawl_temp_file}'
                    cocrawl_out = subprocess.Popen(cocrawl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = cocrawl_out.communicate()

                with open(cocrawl_temp_file, 'r') as f:
                    cocrawl_result = set(f.read().splitlines())

                crawler_temp.update(cocrawl_result)
                subprocess.run(['rm', cocrawl_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(cocrawl_result)) + green + " subdomains.")

            elif tool == 'archive':
                with open(archive_temp_file, 'w') as f:
                    pass
                if crawler_list:
                    archive_command = f'python3 main_tools/tools/archive.py -l {crawler_list} | tee -a {archive_temp_file}'   
                    archive_out = subprocess.Popen(archive_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = archive_out.communicate()
                elif crawler_domain:               
                    archive_command = f'python3 main_tools/tools/archive.py -d {crawler_domain} | tee -a {archive_temp_file}'   
                    archive_out = subprocess.Popen(archive_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = archive_out.communicate()

                with open(archive_temp_file, 'r') as f:
                    archive_result = set(f.read().splitlines())

                crawler_temp.update(archive_result)
                subprocess.run(['rm', archive_temp_file], check=True)  
                print(green + f"{tool} found " + blue + str(len(archive_result)) + green + " subdomains.")           

            elif tool == 'waybackurl':
                with open(waybackurl_temp_file, 'w') as f:
                    pass
                if crawler_list:
                    waybackurl_command = f'cat {crawler_list} | waybackurls | tee -a {waybackurl_temp_file}'      
                    waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = waybackurl_out.communicate()
                elif crawler_domain:
                    waybackurl_command = f'waybackurls {crawler_domain} | tee -a {waybackurl_temp_file}'      
                    waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = waybackurl_out.communicate()

                with open(waybackurl_temp_file, 'r') as f:
                    waybackurl_result = set(f.read().splitlines())

                crawler_temp.update(waybackurl_result)
                subprocess.run(['rm', waybackurl_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(waybackurl_result)) + green + " subdomains.")

            elif tool == 'gau':
                with open(gau_temp_file, 'w') as f:
                    pass
                if crawler_list:
                    gau_command = f'cat {crawler_list} | gau | tee -a {gau_temp_file}'      
                    gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = gau_out.communicate()
                elif crawler_domain:
                    gau_command = f'gau {crawler_domain} | tee -a {gau_temp_file}'      
                    gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = gau_out.communicate()

                with open(gau_temp_file, 'r') as f:
                    gau_result = set(f.read().splitlines())

                crawler_temp.update(gau_result)
                subprocess.run(['rm', gau_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(gau_result)) + green + " subdomains.")
            
            elif tool == 'getjs':
                with open(getJS_temp_file, 'w') as f:
                    pass
                with open(getJS_out_file, 'w') as f:
                    pass
                sed_command= f"sed 's#^#https://#' {crawler_list} > {getJS_temp_file}"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                sed_output, error = sed_out.communicate()
                if crawler_list:
                    with open(getJS_temp_file, 'r') as f:
                        urls = set(f.read().splitlines())
                        for url in urls: 
                            getJS_command = f'getjs --url {url} | tee -a {getJS_out_file}'
                            getJS_out = subprocess.Popen(getJS_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = getJS_out.communicate()
                elif crawler_domain:
                    getJS_command = f'getjs --url {crawler_domain} | tee -a {getJS_out_file}'
                    getJS_out = subprocess.Popen(getJS_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = getJS_out.communicate()
                
                with open(getJS_out_file, 'r') as f:
                    getJS_result = set(f.read().splitlines())
                
                crawler_temp.update(getJS_result)
                subprocess.run(['rm', getJS_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(getJS_result)) + green + " subdomains.")
            
            elif tool == 'katana':
                with open(katana_temp_file, 'w') as f:
                    pass
                if crawler_list:
                    katana_command = f'katana -list {crawler_list} -nc -silent | tee -a {katana_temp_file}'   
                    katana_out = subprocess.Popen(katana_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = katana_out.communicate()
                elif crawler_domain:
                    katana_command = f'katana -u {crawler_domain} -nc -silent | tee -a {katana_temp_file}'   
                    katana_out = subprocess.Popen(katana_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = katana_out.communicate()

                with open(katana_temp_file, 'r') as f:
                    katana_result = set(f.read().splitlines())

                crawler_temp.update(katana_result)
                subprocess.run(['rm', katana_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(katana_result)) + green + " subdomains.")
            
            elif tool == 'cariddi':
                with open(cariddi_temp_file, 'w') as f:
                    pass
                with open(cariddi_out_file, 'w') as f:
                    pass
                sed_command= f"sed 's#^#https://#' {crawler_list} > {cariddi_temp_file}"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                sed_output, error = sed_out.communicate()
                if crawler_list:
                    cariddi_command = f'cat {cariddi_temp_file} | cariddi -plain | tee -a {cariddi_out_file}'   
                    cariddi_out = subprocess.Popen(cariddi_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = cariddi_out.communicate()
                elif crawler_domain:
                    cariddi_command = f'echo https://{crawler_domain} | cariddi -plain | tee -a {cariddi_out_file}'   
                    cariddi_out = subprocess.Popen(cariddi_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = cariddi_out.communicate()
                
                with open(cariddi_out_file, 'r') as f:
                    cariddi_result = set(f.read().splitlines())
                
                crawler_temp.update(cariddi_result)
                subprocess.run(['rm', cariddi_temp_file], check=True)
                subprocess.run(['rm', cariddi_out_file], check=True)
                print(green + f"{tool} found " + blue + str(len(cariddi_result)) + green + " subdomains.")

            
            elif tool == 'hakrawler':
                with open(hakrawler_temp_file, 'w') as f:
                    pass
                with open(hakrawler_out_file, 'w') as f:
                    pass
                sed_command= f"sed 's#^#https://#' {crawler_list} > {hakrawler_temp_file}"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                sed_output, error = sed_out.communicate()
                if crawler_list:
                    hakrawler_command = f'cat {hakrawler_temp_file} | hakrawler -subs | tee -a {hakrawler_out_file}'   
                    hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = hakrawler_out.communicate()
                elif crawler_domain:
                    hakrawler_command = f'echo https://{crawler_domain} |  hakrawler -plain | tee -a {hakrawler_out_file}'   
                    hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = hakrawler_out.communicate()
                
                with open(hakrawler_out_file, 'r') as f:
                    hakrawler_result = set(f.read().splitlines())
                
                crawler_temp.update(hakrawler_result)
                subprocess.run(['rm', hakrawler_temp_file], check=True)
                subprocess.run(['rm', hakrawler_out_file], check=True)
                print(green + f"{tool} found " + blue + str(len(hakrawler_result)) + green + " subdomains.")
            
            elif tool == 'golinkfinder':
                with open(golinkfinder_temp_file, 'w') as f:
                    pass
                if crawler_list:
                    with open(crawler_list, 'r') as f:
                        urls = set(f.read().splitlines())
                        for url in urls: 
                            golinkfinder_command = f'golinkfinder -d {url} | tee -a {golinkfinder_temp_file}'
                            golinkfinder_out = subprocess.Popen(golinkfinder_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = golinkfinder_out.communicate()
                elif crawler_domain:
                    golinkfinder_command = f'golinkfinder -u {crawler_domain} | tee -a {golinkfinder_temp_file}'
                    golinkfinder_out = subprocess.Popen(golinkfinder_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = golinkfinder_out.communicate()

                with open(golinkfinder_temp_file, 'r') as f:
                    golinkfinder_result = set(f.read().splitlines())
                
                crawler_temp.update(golinkfinder_result)
                subprocess.run(['rm', golinkfinder_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(golinkfinder_result)) + green + " subdomains.")

        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

    crawler_temp_out = set(crawler_temp)
    with open(urls_output_temp_file, 'w') as f:
        f.write('\n'.join(crawler_temp_out))
    
    print(colorama.Fore.GREEN + f"Total " + blue + f"{len(crawler_temp_out)}" + green + " URLs found. Successfully printed to the " + blue + f'{urls_output_temp_file}' + green + " file.")
    
    print(colorama.Fore.CYAN + f"Parsing .js URLs on {urls_output_temp_file}")
    try:
        first_sed_command = f"sed -e '/\.js$/d' {urls_output_temp_file} | sort -u"
        first_sed_command_out = subprocess.Popen(first_sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = first_sed_command_out.communicate()

        nonjs_urls = set(output.splitlines())
        with open(urls_output_file, 'w') as f:
            f.write('\n'.join(nonjs_urls))
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"sed returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
    
    try:
        second_sed_command = f"sed -E '/\.js$/!d' {urls_output_temp_file} | sort -u"
        second_sed_command_out = subprocess.Popen(second_sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = second_sed_command_out.communicate()

        withjs_urls = set(output.splitlines())
        with open(urls_output_file_js, 'w') as f:
            f.write('\n'.join(withjs_urls))
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"sed returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
    
    print(green + f"Parsed URLs Successfully printed to the " + blue + f'{urls_output_file}' + green + " and " + blue + f'{urls_output_file_js}' + green + " file.")

    html_output(output_filenmae, urls_output_file, scan_info, output_kind)
    html_output(output_filenmae, urls_output_file_js, scan_info_js, output_kind)
    
    subprocess.run(['rm', urls_output_temp_file], check=True)

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