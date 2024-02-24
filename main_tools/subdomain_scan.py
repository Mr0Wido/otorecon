from main_tools.common_libs import *
from main_tools.html_output import html_output

def parser_arguments():
    parser = argparse.ArgumentParser(description='subdomain discovery tools')
    parser.add_argument('-subs', '--subdomain_scan',help = 'Specify subdomain tools to run or use "all"',nargs = '*', choices = ['sublist3r', 'subfinder', 'assetfinder',  'findomain', 'crtsh','theharvester', 'shuffledns', 'dnsgen', 'wfuzz', 'altdns', 'all'], default=None)
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=False)
    parser.add_argument('-os', '--out_of_scope', help='Out-of-scope domains file path', default=None, required=False)
    return parser.parse_args()

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))
    

def subdomain_scan():
    #Tools
    subdomain_tools = ['subfinder', 'assetfinder', 'findomain', 'sublist3r', 'theharvester', 'crtsh', 'shuffledns', 'dnsgen', 'wfuzz', 'altdns']

    #Variables
    args = parser_arguments()
    domain_name = args.domain_name
    out_of_scope_file = args.out_of_scope
    output_file = f'{domain_name}_subs.txt' 
    other_file = f'{domain_name}_subs_other.txt'
    temp_subdomains = set()
    all_subdomains = set()
    temp_subs_out = set()
    scan_kind = 'subdomains_scan'
    scan_info = 'Subdomain Scan'
    scan_info_other = 'TheHarvester Scan Other Informations'


    if args.subdomain_scan is None:
        print(colorama.Fore.RED + 'The following arguments are required: -subs/--subdomain_scan')
        sys.exit(1)

    if out_of_scope_file is None:
        print(colorama.Fore.RED + 'The following arguments are required: -os/--out_of_scope')
        sys.exit(1)
        
    if domain_name:
        write_to_file(domain_file, domain_name.splitlines())
    
    with open(output_file, 'w') as f:
        pass
    with open(other_file, 'w') as f:
        pass

    for tool in subdomain_tools:
        print(colorama.Fore.CYAN + f"Running {tool} on {domain_name}")
        if tool not in args.subdomain_scan and 'all' not in args.subdomain_scan:
            continue
        
        try:    
            #Subfinder
            if tool =="subfinder":
                output = subprocess.check_output([tool, '-d', domain_name, '-silent']).decode()
                subfinder = set(output.splitlines())
                temp_subdomains.update(subfinder)
                print(green + f"{tool} found " + blue + str(len(subfinder)) + green + " subdomains.")


            #Assetfinder
            elif tool == "assetfinder": 
                output = subprocess.check_output([tool, '-subs-only', domain_name]).decode()
                assetfinder = set(output.splitlines())
                temp_subdomains.update(assetfinder)
                print(green + f"{tool} found " + blue + str(len(assetfinder)) + green + " subdomains.")
            
            #Findomain
            elif tool == "findomain":
                output = subprocess.check_output([tool, '-t', domain_name, '-q']).decode()
                findomain = set(output.splitlines())
                temp_subdomains.update(findomain)
                print(green + f"{tool} found " + blue + str(len(findomain)) + green + " subdomains.")

            #Sublist3r
            elif tool == "sublist3r":
                with open(sublist3r_temp_file, 'w') as f:
                    pass
                output = subprocess.check_output([tool, '-d', domain_name, '-n', '-o', sublist3r_temp_file]).decode()
                with open(sublist3r_temp_file, 'r') as f:
                    sublist3r = set(f.read().splitlines())
                temp_subdomains.update(sublist3r)
                subprocess.run(['rm', sublist3r_temp_file], check=True)
                print(green + f"{tool} found " + blue + str(len(sublist3r)) + green + " subdomains.")
            
            #TheHarvester
            elif tool =="theharvester":
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
                print(green + f"{tool} found " + blue + str(len(theharvester)) + green + " subdomains.")
            #Crt.sh
            elif tool =="crtsh":
                crtsh_command = f'python3 main_tools/tools/crtsh.py -d {domain_name}'
                crtsh_out = subprocess.Popen(crtsh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = crtsh_out.communicate()

                crtsh = set(output.splitlines())
                temp_subdomains.update(crtsh)
                print(green + f"{tool} found " + blue + str(len(crtsh)) + green + " subdomains.")
                
            #Subbrute and Massdns
            elif tool == "shuffledns":
                shuffledns_command = f'shuffledns -d {domain_name} -w main_tools/wordlists/subdomain_wordlists/names.txt -r main_tools/wordlists/subdomain_wordlists/resolvers.txt -nc -silent'
                sub_out = subprocess.Popen(shuffledns_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = sub_out.communicate()

                shuffledns = set(output.splitlines())
                temp_subdomains.update(shuffledns)
                print(green + f"{tool} found " + blue + str(len(shuffledns)) + green + " subdomains.")

            #dnsgen
            elif tool == "dnsgen": 
                with open(dnsgen_temp_file, 'w') as f:
                    pass
                dnsgen_command = f'cat {domain_file} | dnsgen - | massdns -r main_tools/wordlists/subdomain_wordlists/resolvers.txt  -t A -o J --flush 2>/dev/null -w {dnsgen_temp_file}'
                dnsgen_out = subprocess.Popen(dnsgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = dnsgen_out.communicate()

                sed_command = "sed -n 's/{\"name\":\"\\([^\"]*\\).*/\\1/p' dnsgen_temp.txt | sed 's/\\.$//' | sed -e 's/-//g' | sort -u"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = sed_out.communicate()

                dnsgen = set(output.splitlines())
                temp_subdomains.update(dnsgen)
                subprocess.run(['rm', f'{dnsgen_temp_file}'], check=True)
                print(green + f"{tool} found " + blue + str(len(dnsgen)) + green + " subdomains.")
            
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
                print(green + f"{tool} found " + blue + str(len(wfuzz)) + green + " subdomains.")
            
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
                print(green + f"{tool} found " + blue + str(len(altdns)) + green + " subdomains.")

        except subprocess.CalledProcessError as e:
            print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")

    all_subdomains.update(temp_subdomains)
    if out_of_scope_file:
        all_subdomains.update(temp_subs_out)
        try:
            with open(out_of_scope_file, 'r') as f:
                out_of_scope_domains = set(f.read().splitlines())
            print(cyan + "Out-Of-Scope domains removing from finded subdomains.")
            remaining_subdomains = all_subdomains - out_of_scope_domains
            all_subdomains.clear()
            all_subdomains.update(remaining_subdomains)
        
        except Exception as e:
            print(colorama.Fore.RED + f"Something went wrong.: {e}")
        
        with open(output_file, 'w') as f:
            f.write('\n' + '\n'.join(all_subdomains))
        
        print(green + "Totol " + blue + f"{len(all_subdomains)}" + green + " subdomains found. Successfully printed to the " + blue +  f'{output_file}' + green + " file.")

        html_output(domain_name, output_file, scan_info, scan_kind)
        html_output(domain_name, other_file, scan_info_other, scan_kind)


if __name__ == "__main__":
    subdomain_scan()