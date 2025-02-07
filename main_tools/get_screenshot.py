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
    output_filename = apart[0]
    output_file = f'{output_filename}_screenshots'
    screenshots_names = f'{output_filename}_screenshots.txt'
    with open(screenshots_names, 'w') as f:
        pass

    try:
        print(colorama.Fore.CYAN + f'Getting screenshot for {get_screenshot}')
        command = f'gowitness scan file -f {get_screenshot} --threads 50 --screenshot-path {output_file} -q'
        command_output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode()

        with open(screenshots_names, 'w') as file:
            for file_name in os.listdir(output_file):
                if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                    file.write(f'{output_file}/{file_name}\n')

    except subprocess.CalledProcessError as e:
        print(colorama.Fore.RED + f'Error: {e}')

    print(colorama.Fore.GREEN + f'Output file: {output_file}')
    html_output(output_file, screenshots_names, scan_info, output_kind)

if __name__ == '__main__':
    get_screenshot()