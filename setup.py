from setuptools import setup, find_packages

setup(
    name="otorecon",
    version="1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "tqdm",
        "argparse",
        "colorama",
        "tldextract==2.2.3",
        "beautifulsoup4",
        "dnspython",
        "click",
        "py-altdns",
        "dnsgen",
        "sublist3r",
        "subbrute",
        "yagooglesearch==1.10.0",
        "python-whois",
        "fake-useragent",
        "urllib3",
        "uro"
    ],
    entry_points={
        "console_scripts": [
            "otorecon=main_tools.main:main"
        ]
    },
    author='Mr0Wido',
    author_email='furkn.dniz@protonmail.com',
    url='https://github.com/Mr0Wido/otorecon',
    description="OtoRecon - Automated Reconnaissance Toolkit",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)

