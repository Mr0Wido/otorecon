#!/usr/bin/env python3
import sys
import os


main_dir = os.path.dirname(os.path.abspath(__file__))
main_tool_dir = os.path.join(main_dir, "main_tools")
sys.path.append(main_tool_dir)


from main_tools.main import main 

if __name__ == '__main__':
    main()