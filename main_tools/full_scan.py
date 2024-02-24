from main_tools.common_libs import *

def parser_arguments():
    parser = argparse.ArgumentParser(description='Full scan')
    parser.add_argument('-fs', '--full_scan', help='Write a Domain name for Full Scan', action='store', required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

tools = ['basic_scan', 'subdomain_scan', 'filter_scan', 'crawler_scan', 'dirsearch_scan', 'get_endpoint']
subdomain_tools = ['subfinder', 'assetfinder', 'findomain', 'sublist3r', 'theharvester', 'crtsh', 'shuffledns', 'dnsgen', 'wfuzz', 'altdns']
crawler_tools  = ['crawler', 'waymac', 'cocrawl', 'waybackurl', 'archive', 'gau', 'getjs', 'katana', 'cariddi', 'hakrawler', 'golinkfinder']
dirsearch_tools = ['rd1000', 'raft', 'dirm2_3', 'dirsearch']
basic_info_tools = ['dnmasscan', 'whatweb']
param_scan_tools = ['paramspider', 'cleanurls']


def full_scan():
    args = parser_arguments()
    temp_subdomains = set()
    subdomains_output = set()
    filtered_subdomains = set()
    crawler_temp = set()
    crawler_temp_out = set()
    dirsearch_result = set()
    dirsearch_temp = set()
    dirsearch_temp_out = set()
    domain_name = args.full_scan 
    domain_temp = 'domain_temp.txt'
    output_file = f'{domain_name}_subs.txt'
    other_file = f'{domain_name}_subs_other.txt'
    urls_output_file = f'{domain_name}_urls.txt'
    urls_output_file_js = f'{domain_name}_urls_js.txt'
    urls_output_temp_file = 'urls_output_temp.txt'
    filtered_file = f'{domain_name}_filtered.txt'
    directories_output_file = f'{domain_name}_directories.txt'
    basic_info_output = f'{domain_name}_info.txt'
    param_output_file = urls_output_file.replace('.txt', '_param.txt')
    endpointjs_output_file = urls_output_file_js.replace('.txt', '_endpoints.txt')
    crawler_list = filtered_file

    with open (f'{domain_name}.html', 'w') as html_file:
        html_file.write(
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sayfa Başlığı</title>
    <link rel="stylesheet" href="main_tools/tools/style.css">

</head>
<body>          
<div class="top-bar">
<h1>Otorecon Output</h1>
</div>                            
''')


    if domain_name:
        write_to_file(domain_file, domain_name.splitlines())

    if args.full_scan:
        for tool in tools:
            if tool == 'basic_scan':
                with open(domain_temp, 'w') as file:
                    pass
                scan_info = 'Basic Information Scan '
                for basic_tool in tqdm(basic_info_tools, desc=cyan + "Basic Information Scan: ", total=len(basic_info_tools)):
                    try:
                        if basic_tool == 'dnmasscan':
                            dnmasscan = f'python3 main_tools/tools/dnmasscan.py {domain_file} {domain_temp}'
                            sub_out = subprocess.Popen(dnmasscan, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            stdout, stderr = sub_out.communicate()

                            sed_command = "sed -n '/^#/!s/^.*Ports:/Ports:/p' masscan.log"
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output1, stderr = sed_out.communicate()

                            dnmasscan = set(output1.splitlines())
                            with open(basic_info_output, 'w') as file:
                                file.write(f"Ports:\n")
                                for line in dnmasscan:
                                    file.write(f"{line}\n")

                        elif basic_tool == 'whatweb':
                            output = subprocess.check_output(['whatweb', '-v', '--colour=NEVER', '-q', '--no-errors', domain_name]).decode()
                            whatweb = set(output.splitlines())

                            with open(basic_info_output, 'a') as file:
                                file.write(f"WhatWeb:\n")
                                for line in whatweb:
                                    file.write(f"{line}\n")

                    except subprocess.CalledProcessError as e:
                        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
                
                subprocess.run(['rm', domain_temp], check=True)
                subprocess.run(['rm', 'masscan.log'], check=True)
                with open(f'{domain_name}.html', 'a') as html_file:
                    with open(basic_info_output, 'r') as file:
                        html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info + ' ' +  domain_name + '</h2>')
                        html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>') 
                
                print(colorama.Fore.GREEN + f"Basic Information Scan Completed and Results saved in " + blue + f"{basic_info_output}" + green + "file.")

            elif tool == 'subdomain_scan':
                scan_info = f'Subdomains Scan '
                scan_info_other = 'TheHarvester Scan Other Informations'
                for subdomain_tool in tqdm(subdomain_tools, desc=cyan + "Subdomain Discovery Scan: ", total=len(subdomain_tools)):
                    try: 
                        #Subfinder
                        if subdomain_tool == 'subfinder':
                            subfinder = subprocess.check_output([subdomain_tool, '-d', domain_name, '-silent']).decode()
                            temp_subdomains.update(subfinder)
                        #Sublist3r
                        elif subdomain_tool == "assetfinder": 
                            assetfinder = subprocess.check_output([subdomain_tool, '-subs-only', domain_name]).decode()
                            temp_subdomains.update(assetfinder)
                        #Findomain
                        elif subdomain_tool == "findomain":
                            findomain = subprocess.check_output([subdomain_tool, '-t', domain_name, '-q']).decode()
                            temp_subdomains.update(findomain)
                        #Sublist3r
                        elif subdomain_tool == "sublist3r":
                            with open(sublist3r_temp_file, 'w') as f:
                                pass
                            output = subprocess.check_output([subdomain_tool, '-d', domain_name, '-n', '-o', sublist3r_temp_file]).decode()
                            with open(sublist3r_temp_file, 'r') as f:
                                sublist3r = set(f.read().splitlines())
                            temp_subdomains.update(sublist3r)
                            subprocess.run(['rm', sublist3r_temp_file], check=True)
                        #TheHarvester
                        elif subdomain_tool =="theharvester":
                            command = f'theHarvester -d {domain_name} -b anubis,crtsh,dnsdumpster,rapiddns,otx,urlscan,yahoo -f theHarvester_out'
                            output = subprocess.check_output(command, shell=True).decode()
                            with open(f'theHarvester_out.json', 'r') as f:
                                data = f.read()
                                json_data = json.loads(data)
                                theharvester = set(json_data['hosts'])
                                other_data = {key: set(json_data[key]) for key in json_data if key != 'hosts'}
                                with open(f'{other_file}', 'w') as f:
                                    for key, value in other_data.items():
                                        f.write(f"\n{key}:\n")
                                        for item in value:
                                            f.write(f"{item}\n")
                            temp_subdomains.update(theharvester)
                            subprocess.run(['rm', 'theHarvester_out.json'], check=True)
                            subprocess.run(['rm', 'theHarvester_out.xml'], check=True)

                        #Crt.sh
                        elif subdomain_tool =="crtsh":
                            crtsh_command = f'python3 main_tools/tools/crtsh.py -d {domain_name}'
                            crtsh_out = subprocess.Popen(crtsh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = crtsh_out.communicate()
                            crtsh = set(output.splitlines())
                            temp_subdomains.update(crtsh)

                        #Subbrute and Massdns
                        elif subdomain_tool == "submass":
                            shuffledns_command = f'shuffledns -d {domain_name} -w main_tools/wordlists/subdomain_wordlists/names.txt -r main_tools/wordlists/subdomain_wordlists/resolvers.txt -nc -silent'
                            sub_out = subprocess.Popen(shuffledns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = sub_out.communicate()

                            shuffledns = set(output.splitlines())
                            temp_subdomains.update(shuffledns)

                        #dnsgen
                        elif subdomain_tool == "dnsgen": 
                            with open(dnsgen_temp_file, 'w') as f:
                                pass
                            dnsgen_command = f'cat {domain_file} | dnsgen - | massdns -r main_tools/wordlists/resolvers.txt  -t A -o J --flush 2>/dev/null -w {dnsgen_temp_file}'
                            dnsgen_out = subprocess.Popen(dnsgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            stdout, stderr = dnsgen_out.communicate()

                            sed_command = "sed -n 's/{\"name\":\"\\([^\"]*\\).*/\\1/p' dnsgen_temp.txt | sed 's/\\.$//' | sed -e 's/-//g' | sort -u"
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = sed_out.communicate()

                            dnsgen = set(output.splitlines())
                            temp_subdomains.update(dnsgen)
                            subprocess.run(['rm', f'{dnsgen_temp_file}'], check=True)
                        
                        #wfuzz
                        elif tool == "wfuzz":
                            with open(wfuzz_temp_file, 'w') as f:
                                pass

                            wfuzz_command = f'wfuzz -f {wfuzz_temp_file} -Z -w main_tools/wordlists/subdomain_wordlists/all.txt --sc 200,202,204,301,302,307,403 https://FUZZ.{domain_name}'
                            wfuzz_out = subprocess.Popen(wfuzz_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            stdout, stderr = wfuzz_out.communicate()
                            
                            sed_command = f'''sed -n "s/.*\\"\\([^\\"]*\\)\\".*/\\1/p" wfuzz_temp.txt | sed 's/$/.{domain_name}/' '''
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = sed_out.communicate()

                            wfuzz = set(output.splitlines())
                            temp_subdomains.update(wfuzz)
                            subprocess.run(['rm', f'{wfuzz_temp_file}'], check=True)

                        #Altdns
                        elif tool == "altdns":
                            with open(altdns_temp_file, 'w') as f:
                                pass
                            altdns_command = f'altdns -i {domain_file} -o {altdns_temp_file} -w main_tools/wordlists/subdomain_wordlists/words.txt'
                            altdns_out = subprocess.Popen(altdns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            stdout, stderr = altdns_out.communicate()

                            with open(altdns_temp_file, 'r') as f:
                                altdns = set(f.read().splitlines())

                            temp_subdomains.update(altdns)
                            subprocess.run(['rm', altdns_temp_file], check=True)

                        subdomains_output.update(temp_subdomains)
                
                    except subprocess.CalledProcessError as e:
                        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
                    
                temp_subdomains.update(subdomains_output)

                with open(output_file, 'a') as f:
                    f.write('\n' + '\n'.join(temp_subdomains))

                with open(f'{domain_name}.html', 'a') as html_file:
                    with open(output_file, 'r') as file:
                        html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info + ' ' +  domain_name + '</h2>')
                        html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
                    with open(other_file, 'r') as file: 
                        html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info_other + ' ' +  domain_name + '</h2>')
                        html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>') 
                
                print(colorama.Fore.GREEN + f"Totol " + blue + f"{len(temp_subdomains)}" + green +  " subdomains found. Successfully printed to the " + blue + f'{output_file}' + green + " file.")

            elif tool == 'filter_scan':
                scan_info = 'Filtered subdomains: '
                with open(filter_temp_file, 'w') as f:
                    pass

                try:
                    filter_command_sc = f'httpx -l {output_file} -p 443,8443,8080,80 -status-code -nc -o {filter_temp_file}'
                    filter_out = subprocess.Popen(filter_command_sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    with tqdm(desc=cyan + "Filtering: ", unit=cyan + " Domains") as pbar:
                        result_lines = 0  
                        while True:
                            output = filter_out.stdout.readline()
                            if output == '' and filter_out.poll() is not None:
                                break
                            if output:
                                pbar.update(1)  
                                result_lines += 1  
                                
                    sed_command = "sed -E 's/^https:\/\///; s/^http:\/\///; s/\[.*\]//g; s/:[0-9]*$//; s/[[:space:]]*$//' filter_temp.txt | sort -u"
                    sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = sed_out.communicate()

                    filtered_subdomains= set(output.splitlines())

                    with open(filtered_file, 'w') as f:
                        f.write('\n'.join(filtered_subdomains))

                    with open(f'{domain_name}.html', 'a') as html_file:
                        with open(filtered_file, 'r') as file:
                            html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info + ' ' +  domain_name + '</h2>')
                            html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>') 
                    
                    print(colorama.Fore.GREEN + f"Filtred: " + blue + f"{result_lines}" + green +  " domains are saved in " + blue +  f'{filtered_file}' + green + " file.")
                    subprocess.run(['rm', filter_temp_file], check=True)
                
                except subprocess.CalledProcessError as e:
                    print(colorama.Fore.RED + f"Error: {e}")

            elif tool == 'crawler_scan':
                scan_info = 'Crawler Scan Result (Not include .js files): '
                scan_info_js = 'Crawler Scan Result (Only .js files): '
                with open(urls_output_temp_file, 'w') as f:
                    pass
                with open(urls_output_file, 'w') as f:
                    pass
                with open(urls_output_file_js, 'w') as f:
                    pass
                for tool in tqdm(crawler_tools, desc=cyan + "Crawler Scan: ", total=len(crawler_tools)):
                    try:
                        if  tool == 'crawler':
                            with open(crawler_temp_file, 'w') as f:
                                pass

                            crawler_command = f'python3 main_tools/tools/crawler.py -l {crawler_list} -o {crawler_temp_file}'
                            crawler_out = subprocess.Popen(crawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output = crawler_out.communicate()

                            with open(crawler_temp_file, 'r') as f:
                                crawler_result = set(f.read().splitlines())
                                
                            crawler_temp.update(crawler_result)
                            subprocess.run(['rm', crawler_temp_file], check=True)

                        elif tool == 'waymac':
                            with open(waymac_temp_file, 'w') as f:
                                pass

                            waymac_command = f'python3 main_tools/tools/waybackMachine.py -l {crawler_list} -o {waymac_temp_file}'
                            waymac_out = subprocess.Popen(waymac_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = waymac_out.communicate()

                            with open(waymac_temp_file, 'r') as f:
                                waymac_result = set(f.read().splitlines())

                            crawler_temp.update(waymac_result)  
                            subprocess.run(['rm', waymac_temp_file], check=True)

                        elif tool == 'cocrawl':
                            with open(cocrawl_temp_file, 'w') as f:
                                pass
            
                            cocrawl_command = f'python3 main_tools/tools/commoncrawl.py -l {crawler_list} | tee -a {cocrawl_temp_file}'
                            cocrawl_out = subprocess.Popen(cocrawl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = cocrawl_out.communicate()

                            with open(cocrawl_temp_file, 'r') as f:
                                cocrawl_result = set(f.read().splitlines())

                            crawler_temp.update(cocrawl_result)
                            subprocess.run(['rm', cocrawl_temp_file], check=True)

                        elif tool == 'archive':
                            with open(archive_temp_file, 'w') as f:
                                pass
            
                            archive_command = f'python3 main_tools/tools/archive.py -l {crawler_list} | tee -a {archive_temp_file}'   
                            archive_out = subprocess.Popen(archive_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = archive_out.communicate()

                            with open(archive_temp_file, 'r') as f:
                                archive_result = set(f.read().splitlines())

                            crawler_temp.update(archive_result)
                            subprocess.run(['rm', archive_temp_file], check=True)             

                        elif tool == 'waybackurl':
                            with open(waybackurl_temp_file, 'w') as f:
                                pass

                            waybackurl_command = f'cat {crawler_list} | waybackurls  | tee -a {waybackurl_temp_file}'      
                            waybackurl_out = subprocess.Popen(waybackurl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = waybackurl_out.communicate()

                            with open(waybackurl_temp_file, 'r') as f:
                                waybackurl_result = set(f.read().splitlines())

                            crawler_temp.update(waybackurl_result)
                            subprocess.run(['rm', waybackurl_temp_file], check=True)

                        elif tool == 'gau':
                            with open(gau_temp_file, 'w') as f:
                                pass
                
                            gau_command = f'cat {crawler_list} | gau  | tee -a {gau_temp_file}'      
                            gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = gau_out.communicate()

                            with open(gau_temp_file, 'r') as f:
                                gau_result = set(f.read().splitlines())

                            crawler_temp.update(gau_result)
                            subprocess.run(['rm', gau_temp_file], check=True)
                        
                        elif tool ==  "getJS":
                            with open(getJS_temp_file, 'w') as f:
                                pass
                            with open(getJS_out_file, 'w') as f:
                                pass
                            sed_command= f"sed 's#^#https://#' {crawler_list} > {getJS_temp_file}"
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            sed_output, error = sed_out.communicate()
                            with open(getJS_temp_file, 'r') as f:
                                urls = set(f.read().splitlines())
                                for url in urls: 
                                    getJS_command = f'python3 main_tools/tools/getJS.py -u {url} | tee -a {getJS_temp_file}'
                                    getJS_out = subprocess.Popen(getJS_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    output, error = getJS_out.communicate()
                            
                            with open(getJS_temp_file, 'r') as f:
                                getJS_result = set(f.read().splitlines())
                            
                            crawler_temp.update(getJS_result)
                            subprocess.run(['rm', getJS_temp_file], check=True)
                        
                        elif tool == "katana":
                            with open(katana_temp_file, 'w') as f:
                                pass
                            katana_command = f'katana -list {crawler_list} -nc -silent | tee -a {katana_temp_file}'   
                            katana_out = subprocess.Popen(katana_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = katana_out.communicate()
                            with open(katana_temp_file, 'r') as f:
                                katana_result = set(f.read().splitlines())
                            crawler_temp.update(katana_result)
                            subprocess.run(['rm', katana_temp_file], check=True)
                        
                        elif tool == "cariddi":
                            with open(cariddi_temp_file, 'w') as f:
                                pass
                            with open(cariddi_out_file, 'w') as f:
                                pass
                            sed_command= f"sed 's#^#https://#' {crawler_list} > {cariddi_temp_file}"
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            sed_output, error = sed_out.communicate()      

                            cariddi_command = f'cat {cariddi_temp_file} | cariddi -plain | tee -a {cariddi_out_file}'   
                            cariddi_out = subprocess.Popen(cariddi_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = cariddi_out.communicate()

                            with open(cariddi_out_file, 'r') as f:
                                cariddi_result = set(f.read().splitlines())
                            
                            crawler_temp.update(cariddi_result)
                            subprocess.run(['rm', cariddi_temp_file], check=True)
                            subprocess.run(['rm', cariddi_out_file], check=True)

                        elif tool == "hakrawler":
                            with open(hakrawler_temp_file, 'w') as f:
                                pass
                            with open(hakrawler_out_file, 'w') as f:
                                pass
                            sed_command= f"sed 's#^#https://#' {crawler_list} > {hakrawler_temp_file}"
                            sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            sed_output, error = sed_out.communicate()

                            hakrawler_command = f'cat {hakrawler_temp_file} | hakrawler -subs | tee -a {hakrawler_out_file}'   
                            hakrawler_out = subprocess.Popen(hakrawler_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = hakrawler_out.communicate()   

                            with open(hakrawler_out_file, 'r') as f:
                                hakrawler_result = set(f.read().splitlines())
                            
                            crawler_temp.update(hakrawler_result)
                            subprocess.run(['rm', hakrawler_temp_file], check=True)
                            subprocess.run(['rm', hakrawler_out_file], check=True)     

                        elif tool == "golinkfinder":
                            with open(golinkfinder_temp_file, 'w') as f:
                                pass
                            with open(crawler_list, 'r') as f:
                                urls = set(f.read().splitlines())
                                for url in urls: 
                                    golinkfinder_command = f'golinkfinder -d {url} | tee -a {golinkfinder_temp_file}'
                                    golinkfinder_out = subprocess.Popen(golinkfinder_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    output, error = golinkfinder_out.communicate()      

                            with open(golinkfinder_temp_file, 'r') as f:
                                golinkfinder_result = set(f.read().splitlines())
                            
                            crawler_temp.update(golinkfinder_result)
                            subprocess.run(['rm', golinkfinder_temp_file], check=True)                                                                                      
                    except subprocess.CalledProcessError as e:
                        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
                
                crawler_temp_out = set(crawler_temp)
                with open(urls_output_temp_file, 'w') as f:
                    f.write('\n'.join(crawler_temp_out)) 
                
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

                try:
                    scan_info_param = 'Sending URLs to paramspider to get parameters'
                    param_command = f'python3 main_tools/tools/clean_urls.py -u {urls_output_file} -o {param_output_file}'
                    param_out = subprocess.Popen(param_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = param_out.communicate()
                except subprocess.CalledProcessError as e:
                    print(colorama.Fore.RED + f"paramspider returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

                try:
                    scan_info_endpoints = 'Sending URLs to endpoint_finder to get endpoints and info from .js files'
                    with open(urls_output_file_js, 'r') as f:
                        urls = set(f.read().splitlines())
                        for url in urls:
                            list_command = f"python3 main_tools/tools/endpoint_finder.py -u {url} -o {endpointjs_output_file}"
                            list_command_out = subprocess.Popen(list_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            output, error = list_command_out.communicate()
                except subprocess.CalledProcessError as e:
                    print(colorama.Fore.RED + f"endpoint_finder returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
            
                with open(f'{domain_name}.html', 'a') as html_file:
                    with open (urls_output_file, 'r') as file:
                        allines= file.readlines()
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info + ' ' +  domain_name + '</h2><div class="code-block">')
                    for line in allines:
                        html_file.write('<a href="' + line.strip() + '" target="_blank">' + line.strip() + '</a><br>')
                    html_file.write('</div></div>')           
                
                with open(f'{domain_name}.html', 'a') as html_file:
                    with open (urls_output_file_js, 'r') as file:
                        allines= file.readlines()
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info_js + ' ' +  domain_name + '</h2><div class="code-block">')
                    for line in allines:
                        html_file.write('<a href="' + line.strip() + '" target="_blank">' + line.strip() + '</a><br>')
                    html_file.write('</div></div>')

                with open(f'{domain_name}.html', 'a') as html_file:
                    with open (param_output_file, 'r') as file:
                        allines= file.readlines()
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info_param + ' ' +  domain_name + '</h2><div class="code-block">')
                    for line in allines:
                        html_file.write('<a href="' + line.strip() + '" target="_blank">' + line.strip() + '</a><br>')
                    html_file.write('</div></div>')    

                with open(f'{domain_name}.html', 'a') as html_file:
                    with open (endpointjs_output_file, 'r') as file:
                        html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info_endpoints + ' ' +  domain_name + '</h2><div class="code-block">')
                        html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')                     

                subprocess.run(['rm', urls_output_temp_file], check=True)
                print(colorama.Fore.GREEN + f"Totol " + blue +  f"{len(crawler_temp)}" + green + " urls found. Successfully parsed and printed to the " + blue + f'{urls_output_file}, {urls_output_file_js}, {param_output_file}' + green + " and " + blue + f'{endpointjs_output_file}' + green + " file.")               
            
            elif tool == 'dirsearch_scan':
                scan_info = 'Directory Bruteforce: '
                with open(directories_output_file, 'w') as f:
                    pass
                try:
                    with open(filtered_file, 'r') as f:
                        subdomains = set(f.read().splitlines())

                    for subdomain in tqdm(subdomains, desc=cyan + f"Directory bruteforce with rd1000.txt"):
                        command = f'gobuster dir -u https://{subdomain} -w main_tools/wordlists/dirsearch_wordlists/rd1000.txt --no-color --no-error -o rd1000_temp.txt'
                        command_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        output, error = command_out.communicate()

                        with open('rd1000_temp.txt', 'r') as f:
                            temp_results = f.readlines()
                        
                        with open('rd1000.txt', 'w') as f:
                            for line in temp_results:
                                f.write(f'{subdomain}: {line}')
                        
                        with open('rd1000.txt', 'r') as f:
                            temp_out = sorted(f.read().splitlines())

                        dirsearch_temp_out.update(temp_out)

                    dirsearch_temp.update(dirsearch_temp_out)
                    with open('rd1000.txt', 'w') as f:
                        f.write('/n'.join(dirsearch_temp_out))

                except subprocess.CalledProcessError as e:
                    print(colorama.Fore.RED + f"Error: {e}")

                dirsearch_result.update(dirsearch_temp)

                with open(directories_output_file, 'w') as f:
                    f.write('\n'.join(dirsearch_result))
                
                subprocess.run(['rm', 'rd1000_temp.txt'], check=True)
                subprocess.run(['rm', 'rd1000.txt'], check=True)
                with open(f'{domain_name}.html', 'a') as html_file:
                    with open (directories_output_file, 'r') as file:    
                        html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + scan_info + ' ' +  domain_name +'</h2>')
                        html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')

                print(colorama.Fore.GREEN + f"Totol " + blue +  f"{len(dirsearch_temp_out)}" + green + " directories found. Successfully printed to the " + blue + f'{directories_output_file}' + green + " file.")

    with open(f'{domain_name}.html', 'a') as html_file:
        html_file.write('<br><br></body></html>')      
    print(colorama.Fore.LIGHTYELLOW_EX + "All results saved in " + blue + f"{domain_name}.html")

if __name__ == "__main__":
    full_scan()
    