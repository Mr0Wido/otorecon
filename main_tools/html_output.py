from main_tools.common_libs import *
import os
from datetime import datetime

def html_output(output_filename, data_file, info, output_kinds):
    current_dir = os.getcwd()
    html_file_path = os.path.join(current_dir, f'{output_filename}.html')

    file_exists = os.path.exists(html_file_path)

    with open(html_file_path, 'a' if file_exists else 'w') as html_file:
        if not file_exists:
            # Eğer dosya ilk defa oluşturuluyorsa, temel HTML yapısını yaz
            html_file.write(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Scan Results</title>
                <link rel="stylesheet" href="main_tools/tools/style.css">
                <script>
                    function openTab(evt, tabName) {{
                        var i, tabcontent, tablinks;
                        
                        tabcontent = document.getElementsByClassName("tabcontent");
                        for (i = 0; i < tabcontent.length; i++) {{
                            tabcontent[i].style.display = "none";
                        }}
                        
                        tablinks = document.getElementsByClassName("tablinks");
                        for (i = 0; i < tablinks.length; i++) {{
                            tablinks[i].className = tablinks[i].className.replace(" active", "");
                        }}
                        
                        document.getElementById(tabName).style.display = "block";
                        evt.currentTarget.className += " active";
                    }}
                </script>
            </head>
            <body>
                <div class="sidebar">
                    <h2>Scans</h2>
                    <div id="tab-buttons"></div>
                </div>
                <div class="content">
                    <div id="scan-results"></div>
            ''')

        # **Benzersiz Tab ID Oluştur**
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tab_id_base = f"{output_filename}_{timestamp.replace(' ', '_').replace(':', '-')}"
        
        # Daha önce aynı ID varsa numaralandır
        counter = 1
        while f"{tab_id_base}-{counter}" in open(html_file_path).read():
            counter += 1
        tab_id = f"{tab_id_base}-{counter}"

        # **Yeni Butonu Sidebar'a Ekleyelim**
        html_file.write(f'''
            <script>
                var btn = document.createElement("button");
                btn.className = "tablinks";
                btn.innerHTML = "{info} ({timestamp})";
                btn.onclick = function() {{ openTab(event, '{tab_id}'); }};
                document.getElementById("tab-buttons").appendChild(btn);
            </script>
        ''')

        # **Yeni Tarama Sonucunu İçerik Alanına Ekleyelim**
        scan_result_html = f'''
            <div id="{tab_id}" class="tabcontent">
                <h2>{info} - {timestamp}</h2>
                <div class="result-list">
        '''

        # **Dosyadaki İçeriği HTML'e Yazalım**
        with open(data_file, 'r') as file:
            if output_kinds == 'crawler_scan':
                for line in file:
                    scan_result_html += f'<a href="{line.strip()}" target="_blank">{line.strip()}</a><br>'
            elif output_kinds == 'get_screenshot':
                for line in file:
                    scan_result_html += f'<p> (-) {line.strip()}<br><img src="{line.strip()}" width="50%" height="50%"><br></p>'
            else:
                scan_result_html += f'<pre>{file.read()}</pre>'

        scan_result_html += '</div></div>'  # `tabcontent` kapatıldı

        # **Tarama Sonucunu `scan-results` İçine Ekleyelim**
        html_file.write(f'''
            <script>
                var resultDiv = document.createElement("div");
                resultDiv.innerHTML = `{scan_result_html}`;
                document.getElementById("scan-results").appendChild(resultDiv);
            </script>
        ''')

        # Eğer dosya yeni oluşturulduysa, body'yi kapat
        if not file_exists:
            html_file.write('</div></body></html>')

    print(colorama.Fore.LIGHTYELLOW_EX + f" [*] {info} results saved in " + blue + f"{output_filename}.html" + yellow + " file successfully!")
