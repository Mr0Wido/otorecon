from main_tools.common_libs import *
from main_tools.html_output import html_output

def parser_arguments():
    parser = argparse.ArgumentParser(description='Get Screenshot')
    parser.add_argument('-gsc', '--get_screenshot', help='URL file for gowitness', action='store', default=None)
    return parser.parse_args()
    
def get_screenshot():
    args = parser_arguments()
    get_screenshot = args.get_screenshot
    scan_info = 'Get Screenshot '
    output_kind = 'get_screenshot'
    apart = get_screenshot.split('_')
    output_filenmae = apart[0]
    output_file = f'{output_filenmae}_screenshots'
    screenshots_names = f'{output_filenmae}_screenshots.txt'
    with open(screenshots_names, 'w') as f:
        pass

    try:
        command = f'gowitness file -f {get_screenshot} --disable-db -P {output_file}'
        command_output = subprocess.check_output(command, shell=True).decode()

        with open(screenshots_names, 'w') as file:
            for file_name in os.listdir(output_file):
                if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                    file.write(f'{output_file}/{file_name}\n')

    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f'Error: {e}')



    print(colorama.Fore.GREEN + f'Output file: {output_file}')
    html_output(output_filenmae, screenshots_names, scan_info, output_kind)
if __name__ == '__main__':
    get_screenshot()

# aaaa
# if get_screenshot:
#     try:
#         with open(get_screenshot , 'r+') as file:
#             lines = file.readlines()
#             file.seek(0)

#             for line in lines:
#                 if 'https' or 'http' not in line:
#                     file.write(f'https://{line}')
#                 else:
#                     file.write(line)

#             file.truncate()

#     except FileNotFoundError:
#         print(colorama.Fore.RED + f'File {get_screenshot} not found')