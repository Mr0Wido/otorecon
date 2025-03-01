from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CustomInstall(install):
    def run(self):
        try:
            install.run(self)
            self.install_tools()
        except Exception as e:
            print(f"Error: {e}")
            return

    def install_tools(self):
        # Genel paketleri kur
        self.run_command("sudo apt-get install -y unzip curl git golang whatweb python3-pip pipx wfuzz gobuster masscan nmap sed dig")
        self.run_command("python3 -m pip install --upgrade pip setuptools wheel")
        
        # pip düzeltme
        self.run_command("python3 -m pip config set global.break-system-packages true")
        
        # Git ile kurulan bağımlılıklar
        self.run_command("git clone https://github.com/laramies/theHarvester.git && cd theHarvester && pip install -r requirements/base.txt")
        self.run_command("sudo mv theHarvester/ /opt/theHarvester && sudo chmod +x /opt/theHarvester/theHarvester.py && sudo ln -sf /opt/theHarvester/theHarvester.py /usr/local/bin/theHarvester")
        self.run_command("rm -rf theHarvester")
        self.run_command("git clone https://github.com/blechschmidt/massdns.git && cd massdns && make && sudo make install")
        self.run_command("rm -rf massdns")

        # Go tabanlı araçlar
        go_tools = {
            "assetfinder": "github.com/tomnomnom/assetfinder@latest",
            "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "katana": "github.com/projectdiscovery/katana/cmd/katana@latest",
            "hakrawler": "github.com/hakluke/hakrawler@latest",
            "getJS": "github.com/003random/getJS@latest",
            "waybackurls": "github.com/tomnomnom/waybackurls@latest",
            "gau": "github.com/lc/gau/v2/cmd/gau@latest",
            "shuffledns": "github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest",
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "gowitness": "github.com/sensepost/gowitness@latest",
            "dnsx": "github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
            "cero": "github.com/glebarez/cero@latest",
            "scilla": "github.com/edoardottt/scilla/cmd/scilla@latest",
            "unfurl": "github.com/tomnomnom/unfurl@latest"
            }

        for tool, repo in go_tools.items():
            self.run_command(f"go install -v {repo} && sudo cp ~/go/bin/{tool} /usr/bin/{tool}")

        # Findomain (manuel kurulum gerekiyor)
        self.run_command("curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux.zip && unzip findomain-linux.zip && chmod +x findomain && sudo mv findomain /usr/bin/findomain && rm findomain-linux.zip")

    def run_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Komut çalıştırılırken hata oluştu: {e}")
            return

setup(
    name='otorecon',
    version='1.0',
    description='Otorecon, a bugbounty automation tool',
    author='Mr0Wido',
    author_email='furkn.dniz@protonmail.com',
    url='https://github.com/otorecon/otorecon',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "tqdm",
        "argparse",
        "colorama",
        "tldextract",
        "beautifulsoup4",
        "dnspython",
        "click",
        "py-altdns",
        "dnsgen",
        "sublist3r",
        "subbrute",
        "yagooglesearch==1.10.0",
        "python-whois",
        "tldextract",
        "fake-useragent",
        "urllib3",
        "uro"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'otorecon=main_tools.main:main',
        ],
    },
    cmdclass={
        'install': CustomInstall,
    }
)