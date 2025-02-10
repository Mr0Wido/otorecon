from main_tools.common_libs import *
from main_tools.html_output import html_output

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

def parser_arguments():
    parser = argparse.ArgumentParser(description='Basic Information Scan About Domain')
    parser.add_argument('-bs', '--basic_scan', help='Specify tools to run or use "all"', nargs = '*', choices = ['dnmasscan', 'whatweb', 'all'], default=None)
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

    for tool in basic_info_tools:
        print( cyan + f"Running {tool} on {domain_name}")
        if tool not in args.basic_scan and 'all' not in args.basic_scan:
            continue            
        try:
            if tool == 'dnmasscan':
                dnmasscan = f'sudo python3 main_tools/tools/dnmasscan.py {domain_file} {domain_temp}'
                sub_out = subprocess.Popen(dnmasscan, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = sub_out.communicate()

                sed_command = "sed -n '/^#/!s/^.*Ports:/Ports:/p' masscan.log"
                sed_out = subprocess.Popen(sed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output1, stderr = sed_out.communicate()

                dnmasscan = set(output1.splitlines())
                with open(output_file, 'w') as file:
                    file.write(f"Ports:\n")
                    for line in dnmasscan:
                        file.write(f"{line}\n")
                        
                subprocess.run(['rm', 'masscan.log'], check=True)

            elif tool == 'whatweb':
                output = subprocess.check_output(['whatweb', '-v', '--colour=NEVER', '-q', '--no-errors', f"https://{domain_name}"]).decode()
                whatweb = set(output.splitlines())

                with open(output_file, 'a') as file:
                    file.write(f"WhatWeb:\n")
                    for line in whatweb:
                        file.write(f"{line}\n")
        except Exception as e:
            print(e)
    subprocess.run(['rm', domain_temp], check=True)
    print(f'{colorama.Fore.GREEN}Basic Information Scan Completed and Results saved in ' + blue + f'{output_file}' + green +  ' file.')

    html_output(domain_name, output_file, scan_info, scan_kind)

if __name__ == "__main__":
    basic_info_scan()
