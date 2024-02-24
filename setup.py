from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.install_tools()

    def install_tools(self):
        os.system("sudo apt-get install golang-go -y")
        os.system("sudo apt-get install whatweb -y")
        os.system("sudo apt-get install subfinder -y")
        os.system("go install -v github.com/tomnomnom/assetfinder@latest && cp ~/go/bin/assetfinder /usr/bin/assetfinder")
        os.system("curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip && unzip findomain-linux-i386.zip && chmod +x findomain && sudo mv findomain /usr/bin/findomain && sudo rm findomain-linux-i386.zip")
        os.system("sudo apt-get install sublist3r -y")
        os.system("sudo apt-get install theharvester -y")
        os.system("sudo apt-get install massdns -y")
        os.system("sudo apt-get install dnsgen -y")
        os.system("sudo apt-get install altdns -y")
        os.system("sudo apt-get install wfuzz -y")
        os.system("go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && cp ~/go/bin/httpx /usr/bin/httpx")
        os.system("go install github.com/projectdiscovery/katana/cmd/katana@latest && cp ~/go/bin/katana /usr/bin/katana")
        os.system("go install github.com/hakluke/hakrawler@latest && cp ~/go/bin/hakrawler /usr/bin/hakrawler")
        os.system("go install github.com/0xsha/GoLinkFinder@latest && cp ~/go/bin/GoLinkFinder /usr/bin/golinkfinder")
        os.system("go install github.com/003random/getJS@latest && cp ~/go/bin/getJS  /usr/bin/getjs")
        os.system("go install github.com/tomnomnom/waybackurls@latest && cp ~/go/bin/waybackurls  /usr/bin/waybackurls")
        os.system("go install github.com/lc/gau/v2/cmd/gau@latest && cp ~/go/bin/gau  /usr/bin/gau")
        os.system("go install -v github.com/edoardottt/cariddi/cmd/cariddi@latest && cp ~/go/bin/cariddi  /usr/bin/cariddi")
        os.system("go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latestt && cp ~/go/bin/shuffledns  /usr/bin/shuffledns")
        os.system("sudo apt-get install gobuster -y")


setup(
    name='otorecon',
    version='1.0',
    description= 'Otorecon, a bugbounty automation tool',
    author='Mr0Wido',
    author_email='furkn.dniz@protonmail.com',
    url='https://github.com/otorecon/otorecon',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
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