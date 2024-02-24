#!/usr/bin/env python3

import sys
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: {}  input_file dns_output_file [masscan_options]".format(sys.argv[0]))
        print()
        print("  input_file:       path to file containing domain names to resolve and scan")
        print("  dns_output_file:  path to the file to store the DNS lookups in")
        print("  masscan_options:  standard masscan options to use (excluding address range).")
        print("                    If not specified, will run masscan using the defaults of: ")
        print("                    -p1-65535 -oG masscan.log --rate=500")
        print()
        sys.exit()

    dns_out = ""
    ip_adresses = []

    print("[*] Resolving domains...")

    try:
        with open(sys.argv[1], 'r') as input_file:
            for domain in input_file:
                domain = domain.strip()
                dig_results = subprocess.run(["dig", "+short", domain], capture_output=True, text=True).stdout.strip().split('\n')

                dns_out += domain + '\n'
                dns_out += '=' * len(domain) + '\n'

                for address in dig_results:
                    dns_out += address + '\n'
                    ip_adresses.append(address)

                dns_out += '\n'

        with open(sys.argv[2], 'w') as out_file:
            out_file.write(dns_out)
        print("[*] Saved resolved addresses to {} ".format(sys.argv[2]))

        print("[*] Launching masscan...")
        if len(sys.argv) == 3:
            print("[*] Using default options: -p1-65535 -oG masscan.log --rate=500")
            print("------------------------")
            subprocess.run(f"masscan -p1-65535 -oG masscan.log --rate=500 {' '.join(ip_adresses)}", shell=True)
        else:
            print("------------------------")
            subprocess.run(["masscan"] + sys.argv[3:] + ip_adresses)
    
    except KeyboardInterrupt:
        print("\nUser Interrupt.")
        sys.exit()

if __name__ == "__main__":
    main()
