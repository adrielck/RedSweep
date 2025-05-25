
import os
import subprocess
import sys
import json
import csv
import argparse
import logging
from datetime import datetime

def print_ascii_art():
    ascii_art = r"""
     /\    
    /  \   
   / /\ \  
  / ____ \ 
 /_/    \_\
     [A]
    """
    print(ascii_art)

def run_command(command, output_file=None, append=True):
    logging.info(f"Executando: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output_file:
            mode = "a" if append else "w"
            with open(output_file, mode) as f:
                f.write(result.stdout)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Erro ao executar '{command}': {e}")
        return ""

def setup_directory(domain):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"recon_{domain}_{timestamp}"
    os.makedirs(path, exist_ok=True)
    os.makedirs(f"{path}/screenshots", exist_ok=True)
    return path

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def configure_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

def recon(domain, enable_gowitness=True):
    output_dir = setup_directory(domain)
    os.chdir(output_dir)
    configure_logging("debug.log")

    logging.info(f"Iniciando reconhecimento em: {domain}")

    run_command(f"whois {domain}", "whois.txt")
    run_command(f"dig {domain} any +noall +answer", "dns.txt")
    run_command(f"host {domain}", "dns.txt")
    run_command(f"nslookup {domain}", "dns.txt")

    run_command(f"subfinder -d {domain} -silent", "subdomains.txt")
    run_command(f"assetfinder --subs-only {domain}", "subdomains.txt")
    run_command(f"amass enum -d {domain} -silent", "subdomains.txt")
    run_command("sort -u subdomains.txt -o subdomains.txt")

    run_command("httpx -silent -l subdomains.txt -o alive.txt")

    alive_hosts = []
    with open("alive.txt", "r") as f:
        alive_hosts = [line.strip() for line in f if line.strip()]

    for host in alive_hosts:
        run_command(f"nmap -T4 -F {host}", "nmap.txt")

    for host in alive_hosts:
        run_command(f"whatweb {host}", "whatweb.txt")

    for host in alive_hosts:
        run_command(f"echo {host} | waybackurls", "waybackurls.txt")

    if enable_gowitness:
        run_command(f"gowitness file -f alive.txt -P screenshots --no-http", "gowitness.log")

    with open("hakrawler.txt", "w") as hak_out:
        for host in alive_hosts:
            out = run_command(f"echo {host} | hakrawler", append=False)
            hak_out.write(out + "\n")

    data_summary = []
    for host in alive_hosts:
        screenshot = f"screenshots/{host.replace('://','_')}.png" if enable_gowitness else None
        data_summary.append({
            "host": host,
            "screenshot": screenshot
        })

    save_json(data_summary, "report.json")
    logging.info(f"Reconhecimento completo. Resultados em: {output_dir}")

if __name__ == "__main__":
    print_ascii_art()

    parser = argparse.ArgumentParser(description="Script de Reconhecimento Ofensivo")
    parser.add_argument("domain", help="Domínio-alvo para executar o reconhecimento")
    parser.add_argument("--no-gowitness", action="store_true", help="Desativar módulo gowitness")

    args = parser.parse_args()
    recon(args.domain, enable_gowitness=not args.no_gowitness)
