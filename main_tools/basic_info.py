from main_tools.common_libs import *
from main_tools.html_output import html_output
import whois

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

def parser_arguments():
    parser = argparse.ArgumentParser(description='Basic Information Scan About Domain')
    parser.add_argument('-bs', '--basic_scan', help='Specify tools to run or use "all"', nargs = '*', choices = ['dnmasscan', 'whatweb', 'google_dork', 'github_dork', 'whois' ,'all'], default=None)
    parser.add_argument('-d', '--domain_name', help='Domain name to scan', action='store', default=None, required=True)
    return parser.parse_args()

def create_directory_url(domain_name):
    directory_name = domain_name
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    return directory_name

def basic_info_scan():
    args = parser_arguments()
    domain_name = args.domain_name
    basic_scan = args.basic_scan
    domain_temp = 'domain_temp.txt'
    scan_kind = 'basic_info_scan'
    scan_info = 'Basic Information Scan'
    directory = create_directory_url(domain_name)
    output_file = os.path.join(directory, f'{domain_name}_info.txt') 


    if basic_scan and domain_name is None:
        print("Please enter a domain name to scan")
        sys.exit(1)
    
    if domain_name:
        write_to_file(domain_file, domain_name.splitlines())

    with open(domain_temp, 'w') as file:
        pass

    with open(output_file, 'w') as file:
        pass

    basic_info_tools = ['dnmasscan', 'whatweb', 'google_dork', 'github_dork', 'whois']
    for tool in basic_info_tools:
        if tool not in args.basic_scan and 'all' not in args.basic_scan:
            continue            
        print( cyan + f" [*] Running {tool} on " + yellow + f"{domain_name}" )
        try:
            if tool == 'dnmasscan':
                dnmasscan_code = f'sudo python3 main_tools/tools/dnmasscan.py {domain_file} {domain_temp}'
                sub_out = subprocess.Popen(dnmasscan_code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = sub_out.communicate()

                with open('masscan.log', 'r') as file:
                    dnmasscan = file.readlines()

                with open(output_file, 'a') as file:
                    file.write(f"\n //Masscan Results \n")
                    file.write('=' * len("//Masscan Results") + '\n')
                    for line in dnmasscan:
                        file.write(f"{line}\n")

                subprocess.run(['rm', '-f', 'masscan.log'], check=True)

            elif tool == 'whatweb':
                output = subprocess.check_output(['whatweb', '-v', '--colour=NEVER', '-q', '--no-errors', '-a 3' , f"https://{domain_name}"]).decode()
                whatweb = set(output.splitlines())

                with open(output_file, 'a') as file:
                    file.write(f"\n //WhatWeb Results \n")
                    file.write('=' * len("//WhatWeb Results") + '\n')
                    for line in whatweb:
                        file.write(f"{line}\n")
            
            elif tool == 'google_dork':
                google_dork = f'python3 main_tools/tools/dork_hunter.py -d {domain_name}'
                sub_out = subprocess.Popen(google_dork, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = sub_out.communicate()
                with open(output_file, 'a') as file:
                    file.write(f"\n //Google Dork Links \n")
                    file.write('=' * len("//Google Dork Links") + '\n')
                    file.write(stdout)
            
            elif tool == 'github_dork':
                github_dork = f'python3 main_tools/tools/github_dork.py {domain_name}'
                sub_out = subprocess.Popen(github_dork, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                stdout, stderr = sub_out.communicate()
                with open(output_file, 'a') as file:
                    file.write(f"\n //Github Dork Links \n")
                    file.write('=' * len("//Github Dork Links") + '\n')
                    file.write(stdout)
            
            elif tool == 'whois':
                whois_info = whois.whois(f"{domain_name}")
                with open(output_file, 'a') as file:
                    file.write(f"\n //Whois Information \n")
                    file.write('=' * len("//Whois Information") + '\n')
                    file.write(f"{whois_info}\n")

        except Exception as e:
            print(e)

    subprocess.run(['rm', '-f', domain_temp], check=True)
    print(f'{colorama.Fore.GREEN} [*] Basic Information Scan Completed and Results saved in ' + blue + f'{output_file}' + green +  ' file.')

    html_output(domain_name, output_file, scan_info, scan_kind)

if __name__ == "__main__":
    basic_info_scan()
