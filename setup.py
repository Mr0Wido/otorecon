from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform
import subprocess

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.install_tools()

    def install_tools(self):
        distro = platform.system().lower()
        package_manager = None

        # Paket yöneticisini belirle
        if os.path.exists("/etc/debian_version"):  # Debian tabanlı sistemler (Ubuntu, Kali, Mint)
            package_manager = "sudo apt-get install -y"
        elif os.path.exists("/etc/fedora-release"):  # Fedora
            package_manager = "sudo dnf install -y"
        elif os.path.exists("/etc/arch-release"):  # Arch Linux
            package_manager = "sudo pacman -S --noconfirm"
        elif distro == "windows":
            package_manager = "choco install"
        else:
            print("Desteklenmeyen dağıtım!")
            return

        # Genel paketleri kur
        self.run_command(f"{package_manager} golang whatweb python3-pip wfuzz gobuster masscan nmap")

        # pip düzeltme
        self.run_command("python3 -m pip config set global.break-system-packages true")
        
        # Git ile kurulan bağımlılıklar
        self.run_command("git clone https://github.com/aboul3la/Sublist3r.git && cd Sublist3r && pip install -r requirements.txt")
        self.run_command("rm -rf Sublist3r")  
        self.run_command("git clone https://github.com/laramies/theHarvester.git && cd theHarvester && pip install -r requirements/base.txt")
        self.run_command("sudo mv theHarvester/ /opt/theHarvester && sudo chmod +x /opt/theHarvester/theHarvester.py && sudo ln -sf /opt/theHarvester/theHarvester.py /usr/bin/theHarvester")
        self.run_command("git clone https://github.com/blechschmidt/massdns.git && cd massdns && make && sudo make install")
        self.run_command("rm -rf massdns")

        # pip ile kurulan bağımlılıklar
        self.run_command("pip3 install py-altdns")
        self.run_command("pip3 install dnsgen")

        # Go tabanlı araçlar
        go_tools = {
            "assetfinder": "github.com/tomnomnom/assetfinder@latest",
            "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "katana": "github.com/projectdiscovery/katana/cmd/katana@latest",
            "hakrawler": "github.com/hakluke/hakrawler@latest",
            "golinkfinder": "github.com/0xsha/GoLinkFinder@latest",
            "getJS": "github.com/003random/getJS@latest",
            "waybackurls": "github.com/tomnomnom/waybackurls@latest",
            "gau": "github.com/lc/gau/v2/cmd/gau@latest",
            "cariddi": "github.com/edoardottt/cariddi/cmd/cariddi@latest",
            "shuffledns": "github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest",
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "gowitness": "github.com/sensepost/gowitness@latest"
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
        "Click",
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