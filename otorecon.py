#!/usr/bin/env python3
import sys
import os
import subprocess

from main_tools.main import main 

main_dir = os.path.dirname(os.path.abspath(__file__))
main_tool_dir = os.path.join(main_dir, "main_tools")
sys.path.append(main_tool_dir)


def check_dependencies():
    tools = ["wfuzz", "gobuster", "masscan", "hakrawler", "getJS", "waybackurls", "gau", "shuffledns", "subfinder", "gowitness", "dnsx", "cero", "scilla", "unfurl", "massdns", "theHarvester", "findomain"]
    missing_tools = [t for t in tools if subprocess.call(f"which {t}", shell=True) != 0]
    if missing_tools:
        print(f"Missing tools: {', '.join(missing_tools)}")
        print("Please run install.sh to install the necessary tools.")
        exit(1)


if __name__ == '__main__':
    check_dependencies()
    main()

