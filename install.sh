#!/bin/bash

echo " [*] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y unzip curl git golang whatweb python3-pip pipx wfuzz gobuster masscan nmap sed dnsutils

echo " [*] Installing Go tools..."
GO_TOOLS=(
    "github.com/tomnomnom/assetfinder"
    "github.com/projectdiscovery/httpx/cmd/httpx"
    "github.com/projectdiscovery/katana/cmd/katana"
    "github.com/hakluke/hakrawler"
    "github.com/003random/getJS"
    "github.com/tomnomnom/waybackurls"
    "github.com/lc/gau/v2/cmd/gau"
    "github.com/projectdiscovery/shuffledns/cmd/shuffledns"
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
    "github.com/sensepost/gowitness"
    "github.com/projectdiscovery/dnsx/cmd/dnsx"
    "github.com/glebarez/cero"
    "github.com/edoardottt/scilla/cmd/scilla"
    "github.com/tomnomnom/unfurl"
)

for tool in "${GO_TOOLS[@]}"; do
    go install -v "$tool@latest" && sudo cp ~/go/bin/$(basename "$tool") /usr/bin/$(basename "$tool")
done

echo " [*] Cloning and installing Git-based tools..."
git clone https://github.com/laramies/theHarvester.git
sudo mv theHarvester /opt/theHarvester
sudo chmod +x /opt/theHarvester/theHarvester.py
sudo ln -sf /opt/theHarvester/theHarvester.py /usr/local/bin/theHarvester
rm -rf theHarvester

git clone https://github.com/blechschmidt/massdns.git
cd massdns && make && sudo make install
rm -rf massdns

echo " [*] Installing Findomain..."
curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
sudo mv findomain /usr/bin/findomain
rm findomain-linux.zip

echo " [*] All tools installed!"