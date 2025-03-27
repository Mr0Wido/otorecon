from main_tools.common_libs import *
from main_tools.html_output import html_output
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed


warnings.filterwarnings("ignore", category=SyntaxWarning)
def parser_arguments():
    parser = argparse.ArgumentParser(description='subdomain discovery tools')
    parser.add_argument('-subs', '--subdomain_scan',help = 'Specify subdomain tools to run or use "all"',nargs = '*', choices = ['subfinder', 'assetfinder',  'findomain', 'crtsh','theharvester', 'cero', 'scilla', 'dnsx', 'shuffledns', 'dnsgen', 'altdns', 'gau' ,'all'], default=None)
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-f', '--file', help='File containing domain names to scan', action='store', default=None, required=False)
    parser.add_argument('-os', '--out_of_scope', help='Out-of-scope domains file path', default=None, required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

#! Create directories  
def create_directory_from_url(domain_name):
    directory_name = domain_name

    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    return directory_name

def create_directory_from_domain_list(domain_list):
    directory_name = domain_list.split('.')[0]

    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    return directory_name

def run_passive_subdomain_tools(tool, domain_name, temp_subdomains, temp_subs_out, out_of_scope_file, other_file, domain_file, domain_list):
    try:   
        if domain_name: 
            ## Subfinder
            if tool =="subfinder":
                output = subprocess.check_output([tool, '-d', domain_name, '-silent']).decode()
                subfinder = set(output.splitlines())
                temp_subdomains.update(subfinder)
                print(green + f"    [+] {tool} found " + blue + str(len(subfinder)) + green + " subdomains.")


            ## Assetfinder
            elif tool == "assetfinder": 
                output = subprocess.check_output([tool, '-subs-only', domain_name], stderr=subprocess.DEVNULL).decode()
                assetfinder = set(output.splitlines())
                temp_subdomains.update(assetfinder)
                print(green + f"    [+] {tool} found " + blue + str(len(assetfinder)) + green + " subdomains.")
        

            ## Findomain
            elif tool == "findomain":
                output = subprocess.check_output([tool, '-t', domain_name, '-q']).decode()
                findomain = set(output.splitlines())
                temp_subdomains.update(findomain)
                print(green + f"    [+] {tool} found " + blue + str(len(findomain)) + green + " subdomains.")
            
            ## TheHarvester
            elif tool =="theharvester":
                theharvester_other = set()
                theharvester = set()
                command = f'theHarvester -d {domain_name} -b anubis,baidu,bing,bingapi,brave,certspotter,crtsh,duckduckgo,hackertarget,otx,rapiddns,sitedossier,subdomaincenter,subdomainfinderc99,threatminer,urlscan,yahoo  -f theHarvester_out >> {theHarvester_temp_file}'
                output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode()
                with open(f'theHarvester_out.json', 'r') as f:
                    data = f.read()
                    json_data = json.loads(data)
                    theharvester = set(json_data['hosts'])
                temp_subdomains.update(theharvester)
                sed_command = f"sed -i -n '/\\[\\*\\] ASNS found:/,$p' {theHarvester_temp_file}"
                subprocess.run(sed_command, shell=True, check=True)
                with open (theHarvester_temp_file, 'r') as f:
                    theharvester_other = f.read()
                
                with open(other_file, 'w') as f:
                    f.write(f"\n TheHarvester: \n")
                    f.write('=' * len("TheHarvester") + '\n')
                    f.write(f"{theharvester_other}\n")

                subprocess.run(['rm', '-f', 'theHarvester_out.json'], check=True)
                subprocess.run(['rm', '-f', 'theHarvester_out.xml'], check=True)
                subprocess.run(['rm', '-f', theHarvester_temp_file], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(theharvester)) + green + " subdomains.")
            
            ## Crt.sh
            elif tool =="crtsh":
                crtsh_command = f'python3 main_tools/tools/crtsh.py -d {domain_name}'
                crtsh_out = subprocess.Popen(crtsh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = crtsh_out.communicate()

                crtsh = set(output.splitlines())
                temp_subdomains.update(crtsh)
                print(green + f"    [+] {tool} found " + blue + str(len(crtsh)) + green + " subdomains.")
            
            ## Cero
            elif tool == "cero":
                cero_command = f'cero {domain_name}'
                cero_out = subprocess.Popen(cero_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = cero_out.communicate()

                cero = set(output.splitlines())
                temp_subdomains.update(cero)
                print(green + f"    [+] {tool} found " + blue + str(len(cero)) + green + " subdomains.")

            ## Scilla
            elif tool == "scilla":
                scilla_command = f'scilla subdomain -target {domain_name} -ot {scilla_temp_file}'
                scilla_out = subprocess.Popen(scilla_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = scilla_out.communicate()

                with open(scilla_temp_file, 'r') as f:
                    scilla = set(f.read().splitlines())
                temp_subdomains.update(scilla)
                subprocess.run(['rm', '-f', f'{scilla_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(scilla)) + green + " subdomains.")
            
            ## Gau
            elif tool == "gau":
                gau_command = f'gau --subs {domain_name} | unfurl -u domains'
                gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = gau_out.communicate()

                gau = set(output.splitlines())
                temp_subdomains.update(gau)
                print(green + f"    [+] {tool} found " + blue + str(len(gau)) + green + " subdomains.")
            
        elif domain_list:
            ## Subfinder
            if tool =="subfinder":
                output = subprocess.check_output([tool, '-dL', domain_list, '-silent']).decode()
                subfinder = set(output.splitlines())
                temp_subdomains.update(subfinder)
                print(green + f"    [+] {tool} found " + blue + str(len(subfinder)) + green + " subdomains.")

            ## Assetfinder
            elif tool == "assetfinder":
                with open(domain_list, 'r') as f:
                    domains = f.read().splitlines()
                for domain in domains:
                    output = subprocess.check_output([tool, '-subs-only', domain], stderr=subprocess.DEVNULL).decode()
                    assetfinder = set(output.splitlines())
                    temp_subdomains.update(assetfinder)
                    
                print(green + f"    [+] {tool} found " + blue + str(len(assetfinder)) + green + " subdomains.")

            ## Findomain
            elif tool == "findomain":
                output = subprocess.check_output([tool, '-f', domain_list, '-q']).decode()
                findomain = set(output.splitlines())
                temp_subdomains.update(findomain)
                print(green + f"    [+] {tool} found " + blue + str(len(findomain)) + green + " subdomains.")
            
            ## TheHarvester
            elif tool =="theharvester":
                with open(domain_list, 'r') as f:
                    domains = f.read().splitlines()
                theharvester_other = set()
                theharvester = set()
                for domain in domains:
                    command = f'theHarvester -d {domain} -b anubis,baidu,bing,bingapi,brave,certspotter,crtsh,duckduckgo,hackertarget,otx,rapiddns,sitedossier,subdomaincenter,subdomainfinderc99,threatminer,urlscan,yahoo  -f theHarvester_out >> {theHarvester_temp_file}'
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode()
                    with open(f'theHarvester_out.json', 'r') as f:
                        data = f.read()
                        json_data = json.loads(data)
                        theharvester = set(json_data['hosts'])
                    temp_subdomains.update(theharvester)
                    sed_command = f"sed -i -n '/\\[\\*\\] ASNS found:/,$p' {theHarvester_temp_file}"
                    subprocess.run(sed_command, shell=True, check=True)
                    with open (theHarvester_temp_file, 'r') as f:
                        theharvester_other = f.read()

                    with open(other_file, 'w') as f:
                        f.write(f"\n TheHarvester: \n")
                        f.write('=' * len("TheHarvester") + '\n')
                        f.write(f"{theharvester_other}\n")

                    subprocess.run(['rm', '-f', 'theHarvester_out.json'], check=True)
                    subprocess.run(['rm', '-f', 'theHarvester_out.xml'], check=True)
                    subprocess.run(['rm', '-f', theHarvester_temp_file], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(theharvester)) + green + " subdomains.")

            ## Crt.sh
            elif tool =="crtsh":
                with open(domain_list, 'r') as f:
                    domains = f.read().splitlines()
                for domain in domains:
                    crtsh_command = f'python3 main_tools/tools/crtsh.py -d {domain}'
                    crtsh_out = subprocess.Popen(crtsh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                    output, error = crtsh_out.communicate()

                    crtsh = set(output.splitlines())
                    temp_subdomains.update(crtsh)
                print(green + f"    [+] {tool} found " + blue + str(len(crtsh)) + green + " subdomains.")
            
            ## Cero
            elif tool == "cero":
                with open(domain_list, 'r') as f:
                    domains = f.read().splitlines()
                for domain in domains:
                    cero_command = f'cero {domain}'
                    cero_out = subprocess.Popen(cero_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                    output, error = cero_out.communicate()

                    cero = set(output.splitlines())
                    temp_subdomains.update(cero)
                print(green + f"    [+] {tool} found " + blue + str(len(cero)) + green + " subdomains.")
                
            ## Scilla
            elif tool == "scilla":
                with open(domain_list, 'r') as f:
                    domains = f.read().splitlines()
                for domain in domains:
                    scilla_command = f'scilla subdomain -target {domain} -ot {scilla_temp_file}'
                    scilla_out = subprocess.Popen(scilla_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                    output, error = scilla_out.communicate()

                    with open(scilla_temp_file, 'r') as f:
                        scilla = set(f.read().splitlines())
                    temp_subdomains.update(scilla)
                    subprocess.run(['rm', '-f', f'{scilla_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(scilla)) + green + " subdomains.")

            ## Gau
                gau_command = f'cat {domain_list} | gau --subs  | unfurl -u domains'
                gau_out = subprocess.Popen(gau_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = gau_out.communicate()

                gau = set(output.splitlines())
                temp_subdomains.update(gau)
                print(green + f"    [+] {tool} found " + blue + str(len(gau)) + green + " subdomains.")
    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")



def run_bruteforce_subdomain_tools (tool, domain_name, temp_subdomains, temp_subs_out, out_of_scope_file, other_file, domain_file, domain_list):
    try:
        if domain_name:
            ## Dnsx
            if tool == "dnsx":
                first_dnsx_command = f'cat {domain_file} | dnsx -recon -silent -nc'
                first_dnsx_out = subprocess.Popen(first_dnsx_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = first_dnsx_out.communicate()

                first_dnsx = set(output.splitlines())
                with open(f'{other_file}', 'a') as f:
                    f.write(f"\n DNSX: \n")
                    f.write('=' * len("DNSX") + '\n')
                    for line in first_dnsx:
                        f.write(f"{line}\n")

                second_dnsx_command = f'dnsx -silent -d {domain_file} -w main_tools/wordlists/subdomain_wordlists/list_sub.txt'
                second_dnsx_out = subprocess.Popen(second_dnsx_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = second_dnsx_out.communicate()

                second_dnsx = set(output.splitlines())
                temp_subdomains.update(second_dnsx)
                print(green + f"    [+] {tool} found " + blue + str(len(second_dnsx)) + green + " subdomains.")
                
            ## shuffledns
            elif tool == "shuffledns":
                puredns_command = f'shuffledns -d {domain_name} -w main_tools/wordlists/subdomain_wordlists/all.txt -r main_tools/wordlists/subdomain_wordlists/resolvers.txt -t 4000 -mode bruteforce -silent -o {shuffledns_temp_file}'
                puredns_out = subprocess.Popen(puredns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = puredns_out.communicate()

                with open(shuffledns_temp_file, 'r') as f:
                    shuffledns = set(f.read().splitlines())
                temp_subdomains.update(shuffledns)
                subprocess.run(['rm', '-f', f'{shuffledns_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(shuffledns)) + green + " subdomains.")

            ## dnsgen
            elif tool == "dnsgen": 
                with open(dnsgen_temp_file, 'w') as f:
                    pass
                dnsgen_command = f'cat {domain_file} | dnsgen - | massdns -r main_tools/wordlists/subdomain_wordlists/resolvers.txt  -t A -o J --flush 2>/dev/null -w {dnsgen_temp_file}'
                dnsgen_out = subprocess.Popen(dnsgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = dnsgen_out.communicate()

                sed_command = "sed -n 's/{\"name\":\"\\([^\"]*\\).*/\\1/p' dnsgen_temp.txt | sed 's/\\.$//' | sed -e 's/-//g' | sort -u"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = sed_out.communicate()

                dnsgen = set(output.splitlines())
                temp_subdomains.update(dnsgen)
                subprocess.run(['rm', '-f', f'{dnsgen_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(dnsgen)) + green + " subdomains.")
            
            ## Altdns
            elif tool == "altdns":
                with open(altdns_temp_file, 'w') as f:
                    pass
                altdns_command = f'altdns -i {domain_file} -o {altdns_temp_file} -w main_tools/wordlists/subdomain_wordlists/words.txt -r -s {altdns_resolved_file}'
                altdns_out = subprocess.Popen(altdns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = altdns_out.communicate()

                sed_command = f"sed 's/:.*//' {altdns_resolved_file} | sort -u"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = sed_out.communicate()

                altdns = set(output.splitlines())
                temp_subdomains.update(altdns)
                subprocess.run(['rm', '-f', altdns_temp_file], check=True)
                subprocess.run(['rm', '-f', altdns_resolved_file], check=True)

                print(green + f"    [+] {tool} found " + blue + str(len(altdns)) + green + " subdomains.")
            
        elif domain_list:
            ## Dnsx
            if tool == "dnsx":
                first_dnsx_command = f'cat {domain_list} | dnsx -recon -silent -nc'
                first_dnsx_out = subprocess.Popen(first_dnsx_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = first_dnsx_out.communicate()

                first_dnsx = set(output.splitlines())
                with open(f'{other_file}', 'a') as f:
                    f.write(f"\n DNSX: \n")
                    f.write('=' * len("DNSX") + '\n')
                    for line in first_dnsx:
                        f.write(f"{line}\n")

                second_dnsx_command = f'dnsx -silent -d {domain_list} -w main_tools/wordlists/subdomain_wordlists/list_sub.txt'
                second_dnsx_out = subprocess.Popen(second_dnsx_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = second_dnsx_out.communicate()

                second_dnsx = set(output.splitlines())
                temp_subdomains.update(second_dnsx)
                print(green + f"    [+] {tool} found " + blue + str(len(second_dnsx)) + green + " subdomains.")

            ## shuffledns
            elif tool == "shuffledns":
                puredns_command = f'shuffledns -l {domain_list} -w main_tools/wordlists/subdomain_wordlists/all.txt -r main_tools/wordlists/subdomain_wordlists/resolvers.txt -t 4000 -mode bruteforce -silent -o {shuffledns_temp_file}'
                puredns_out = subprocess.Popen(puredns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = puredns_out.communicate()

                with open(shuffledns_temp_file, 'r') as f:
                    shuffledns = set(f.read().splitlines())
                temp_subdomains.update(shuffledns)
                subprocess.run(['rm', '-f', f'{shuffledns_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(shuffledns)) + green + " subdomains.")

            ## dnsgen
            elif tool == "dnsgen": 
                with open(dnsgen_temp_file, 'w') as f:
                    pass
                dnsgen_command = f'cat {domain_list} | dnsgen - | massdns -r main_tools/wordlists/subdomain_wordlists/resolvers.txt  -t A -o J --flush 2>/dev/null -w {dnsgen_temp_file}'
                dnsgen_out = subprocess.Popen(dnsgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = dnsgen_out.communicate()

                sed_command = "sed -n 's/{\"name\":\"\\([^\"]*\\).*/\\1/p' dnsgen_temp.txt | sed 's/\\.$//' | sed -e 's/-//g' | sort -u"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = sed_out.communicate()

                dnsgen = set(output.splitlines())
                temp_subdomains.update(dnsgen)
                subprocess.run(['rm', '-f', f'{dnsgen_temp_file}'], check=True)
                print(green + f"    [+] {tool} found " + blue + str(len(dnsgen)) + green + " subdomains.")

            ## Altdns
            elif tool == "altdns":
                with open(altdns_temp_file, 'w') as f:
                    pass
                altdns_command = f'altdns -i {domain_list} -o {altdns_temp_file} -w main_tools/wordlists/subdomain_wordlists/words.txt -r -s {altdns_resolved_file}'
                altdns_out = subprocess.Popen(altdns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = altdns_out.communicate()

                sed_command = f"sed 's/:.*//' {altdns_resolved_file} | sort -u"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                output, error = sed_out.communicate()

                altdns = set(output.splitlines())
                temp_subdomains.update(altdns)
                subprocess.run(['rm', '-f', altdns_temp_file], check=True)
                subprocess.run(['rm', '-f', altdns_resolved_file], check=True)

                print(green + f"    [+] {tool} found " + blue + str(len(altdns)) + green + " subdomains.")

    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

def subdomain_scan():
    #! Tools
    subdomain_tools = ['subfinder', 'assetfinder', 'findomain', 'theharvester', 'crtsh', 'shuffledns', 'dnsgen', 'altdns','gau', 'cero', 'scilla', 'dnsx']

    #! Variables
    args = parser_arguments()
    domain_name = args.domain_name
    domain_list = args.file
    out_of_scope_file = args.out_of_scope

    temp_subdomains = set()
    all_subdomains = set()
    temp_subs_out = set()
    scan_kind = 'subdomains_scan'
    scan_info = 'Subdomain Scan'
    scan_info_other = 'TheHarvester Scan Other Informations'

    if domain_name:
        directory = create_directory_from_url(domain_name)
        output_file = os.path.join(directory, f'{domain_name}_subs.txt') 
        other_file = os.path.join(directory, f'{domain_name}_subs_other.txt')
    
    elif domain_list:
        directory = create_directory_from_domain_list(domain_list)
        output_file = os.path.join(directory, f'{domain_list}_subs.txt') 
        other_file = os.path.join(directory, f'{domain_list}_subs_other.txt')


    if args.subdomain_scan is None:
        print(colorama.Fore.RED + 'The following arguments are required: -subs/--subdomain_scan')
        sys.exit(1)

    if out_of_scope_file is None:
        print(colorama.Fore.RED + 'The following arguments are required: -os/--out_of_scope')
        sys.exit(1)
        
    if domain_name:
        write_to_file(domain_file, domain_name.splitlines())
        
    
    #! Create files
    with open(output_file, 'w') as f:
        pass
    with open(other_file, 'w') as f:
        pass


    print(colorama.Fore.CYAN + f" [*] Running tools on " + green + f"{domain_name or domain_file} " )
    
    #! PASSIVE SUBDOMAIN SCAN
    max_threads = (min(4, len(subdomain_tools)))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        for tool in subdomain_tools:
            if tool not in args.subdomain_scan and 'all' not in args.subdomain_scan:
                continue
            futures.append(executor.submit(run_passive_subdomain_tools, tool, domain_name, temp_subdomains, temp_subs_out, out_of_scope_file, other_file, domain_file, domain_list))

        for future in as_completed(futures):
            future.result()

    #! BRUTEFORCE SUBDOMAIN SCAN
    max_threads = (min(4, len(subdomain_tools)))
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        for tool in subdomain_tools:
            if tool not in args.subdomain_scan and 'all' not in args.subdomain_scan:
                continue
            futures.append(executor.submit(run_bruteforce_subdomain_tools, tool, domain_name, temp_subdomains, temp_subs_out, out_of_scope_file, other_file, domain_file, domain_list))

        for future in as_completed(futures):
            future.result()
    
    #! Printıng Other Information Results
    for tool in subdomain_tools:
        if tool not in args.subdomain_scan and 'all' not in args.subdomain_scan:
            continue 
        if tool == "theharvester":
            print(green + " [*] TheHarvester other results saved in " + blue + f'{other_file}' + green + " file.")
            html_output(domain_name, other_file, scan_info_other, scan_kind)
        if tool == "dnsx":
            print(green + " [*] DNSX other results saved in " + blue + f'{other_file}' + green + " file.")
            html_output(domain_name, other_file, scan_info_other, scan_kind)
        if tool == "theharvester" and tool == "dnsx":
            print(green + " [*] TheHarvester and DNSX other results saved in " + blue + f'{other_file}' + green + " file.")
            html_output(domain_name, other_file, scan_info_other, scan_kind)

    #! Removing Out-Of-Scope Domains and Printing Results
    all_subdomains.update(temp_subdomains)
    if out_of_scope_file:
        all_subdomains.update(temp_subs_out)
        try:
            with open(out_of_scope_file, 'r') as f:
                out_of_scope_domains = set(f.read().splitlines())
            print(cyan + "    [-] Out-Of-Scope domains removing from finded subdomains.")
            remaining_subdomains = all_subdomains - out_of_scope_domains
            all_subdomains.clear()
            all_subdomains.update(remaining_subdomains)
        
        except Exception as e:
            print(colorama.Fore.RED + f"Something went wrong.: {e}")
        
        with open(output_file, 'w') as f:
            f.write('\n' + '\n'.join(all_subdomains))
        
        print(green + " [*] Total " + blue + f"{len(all_subdomains)}" + green + " subdomains found. Successfully printed to the " + blue + f'{output_file}' + green + " file.")
    
        html_output(domain_name, output_file, scan_info, scan_kind)
        

if __name__ == "__main__":
    subdomain_scan()