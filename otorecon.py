#!/usr/bin/env python3
import sys
import os
import subprocess

from main_tools.main import main 

main_dir = os.path.dirname(os.path.abspath(__file__))
main_tool_dir = os.path.join(main_dir, "main_tools")
sys.path.append(main_tool_dir)

if __name__ == '__main__':
    main()

