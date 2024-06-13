#=========================================================#
# [+] Title: Look-up tool to search up IPs from websites  #
# [+] Script: dns_lookup_tool.py                          #
# [+] Blog: https://github.com/b0mb3rexe                  #
# [+] Discord: https://discord.gg/GRnwsUWEch
# [+] Message to Skids: if u skid this please give creds  #
#=========================================================#

import sys
import time
import socket
import threading
import dns.resolver
from rich.console import Console
from rich.table import Table
from optparse import OptionParser

LOGO = r'''
 __       ______   ______   ___   ___            __  __   ______
/_/\     /_____/\ /_____/\ /___/\/__/\          /_/\/_/\ /_____/\  
\:\ \    \:::_ \ \\:::_ \ \\::.\ \\ \ \  _______\:\ \:\ \\:::_ \ \ 
 \:\ \    \:\ \ \ \\:\ \ \ \\:: \/_) \ \/______/\\:\ \:\ \\:(_) \ \
  \:\ \____\:\ \ \ \\:\ \ \ \\:. __  ( (\__::::\/ \:\ \:\ \\: ___\/
   \:\/___/\\:\_\ \ \\:\_\ \ \\: \ )  \ \          \:\_\:\ \\ \ \  
    \_____\/ \_____\/ \_____\/ \__\/\__\/           \_____\/ \_\/  
'''

DEVELOPER_INFO = '''
Developer: #B0MB3R
Contact: https://github.com/b0mb3rexe
Discord: https://discord.gg/bfmPbpCr
'''

console = Console()

def banner():
    console.clear()
    console.print(LOGO, style="bold green")

def fetch_dns_info(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.to_text() for ip in result]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return []

def display_dns_info(domains_info):
    table = Table(title="DNS Information")
    table.add_column("Domain", style="bold yellow")
    table.add_column("IP Addresses", style="bold green")

    for domain, ips in domains_info.items():
        table.add_row(domain, ", ".join(ips))

    console.print(table)

def dns_lookup(domains, threads):
    domains_info = {}
    lock = threading.Lock()

    def worker(domains):
        for domain in domains:
            ips = fetch_dns_info(domain)
            with lock:
                domains_info[domain] = ips

    if not domains:
        return domains_info

    # Split domains into chunks for each thread
    chunk_size = max(1, len(domains) // threads)
    chunks = [domains[i:i + chunk_size] for i in range(0, len(domains), chunk_size)]

    thread_list = []
    for chunk in chunks:
        thread = threading.Thread(target=worker, args=(chunk,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    return domains_info

def show_developer_info():
    console.print(DEVELOPER_INFO, style="bold blue")

def main():
    banner()

    parser = OptionParser()
    parser.add_option('-t', '--threads', dest='threads', type=int, default=1, metavar='N', help='Number of threads (default=1)')
    options, _ = parser.parse_args()

    while True:
        console.print("1) DNS Lookup")
        console.print("2) Developer")
        console.print("3) Exit\n")

        choice = console.input("Choose an option: ")

        if choice == '1':
            domains_file = console.input("Enter the domain file path: ").strip()

            try:
                with open(domains_file, 'r') as f:
                    domains = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                console.print(f"[bold red]File not found: {domains_file}[/bold red]")
                continue

            if not domains:
                console.print(f"[bold red]No domains to lookup.[/bold red]")
                continue

            start_time = time.time()
            console.print(f"[bold blue]Starting DNS lookup for {len(domains)} domains with {options.threads} threads...[/bold blue]")

            domains_info = dns_lookup(domains, options.threads)

            display_dns_info(domains_info)

            console.print(f"[bold blue]Completed in {time.time() - start_time:.2f} seconds[/bold blue]")

        elif choice == '2':
            show_developer_info()

        elif choice == '3':
            console.print("[bold green]Exiting the tool. Goodbye![/bold green]")
            break

        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == '__main__':
    main()
