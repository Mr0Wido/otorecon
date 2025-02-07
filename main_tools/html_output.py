from main_tools.common_libs import *


def html_output(output_filename, data_file, info, output_kinds):
    current_dir = os.getcwd()
    html_file_path = os.path.join(current_dir, f'{output_filename}.html')

    if not os.path.exists(html_file_path):
        with open (html_file_path, 'w') as html_file:
            html_file.write(
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sayfa Başlığı</title>
    <link rel="stylesheet" href="main_tools/tools/style.css">

</head>
<body>          
<div class="top-bar">
<h1>Otorecon Output</h1>
</div>                            
'''
)
            if output_kinds == 'subdomains_scan':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>') 
            elif output_kinds == 'filter_scan':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'crawler_scan':
                with open (data_file, 'r') as file:
                    allines= file.readlines()
                html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2><div class="code-block">')
                for line in allines:
                    html_file.write('<a href="' + line.strip() + '" target="_blank">' + line.strip() + '</a><br>')
                html_file.write('</div></div>')                  
            elif output_kinds == 'dirsearch_scan':
                with open (data_file, 'r') as file:    
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename +'</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'endpoint_finder':
                with open (data_file, 'r') as file:    
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename +'</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'basic_info_scan':
                with open (data_file, 'r') as file:    
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename +'</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'get_screenshot':
                with open (data_file, 'r') as file:
                    allines= file.readlines()
                html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2><div class="code-block">')
                for line in allines:
                    html_file.write('<p> (-) ' + line.strip() + '<br><img src="' + line.strip() + '" width="50%" height="50%"><br></p>')
                html_file.write('</div></div>')

    
    elif os.path.exists(html_file_path):
        with open (html_file_path, 'a') as html_file:
            if output_kinds == 'subdomains_scan':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>') 
            elif output_kinds == 'filter_scan':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'crawler_scan':
                with open (data_file, 'r') as file:
                    allines= file.readlines()
                html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2><div class="code-block">')
                for line in allines:
                    html_file.write('<a href="' + line.strip() + '" target="_blank">' + line.strip() + '</a><br>')
                html_file.write('</div></div>')    
            elif output_kinds == 'dirsearch_scan':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' + output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'endpoint_finder':
                with open (data_file, 'r') as file:
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' + output_filename + '</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'basic_info_scan':
                with open (data_file, 'r') as file:    
                    html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename +'</h2>')
                    html_file.write('<div class="code-block"><pre>' + file.read() + '</pre></div></div>')
            elif output_kinds == 'get_screenshot':
                with open (data_file, 'r') as file:
                    allines= file.readlines()
                html_file.write('<div class="title"><h2 style="text-align: left; margin-left: 30px;">' + info + ' ' +  output_filename + '</h2><div class="code-block">')
                for line in allines:
                    html_file.write('<p> (-) ' + line.strip() + '<br><img src="' + line.strip() + '" width="50%" height="50%"><br></p>')
                html_file.write('</div></div>')

            html_file.write('<br><br></body></html>')      
    print(colorama.Fore.LIGHTYELLOW_EX + f"{info} results saved in " + blue + f"{output_filename}.html"  + yellow + " file successfully!")

