from datetime import datetime


def generate_ruler():
    return '==============================================================='


def generate_banner(url, threads, wordlist_path, codes, user_agent, timeout):
    return (
        f'===============================================================\n'
        f'Pybuster v0.1\n'
        f'by Leo Kontogiorgis (leo@konto.dev)\n'
        f'===============================================================\n'
        f'[+] Mode         : dir\n'
        f'[+] URL          : {url}\n'
        f'[+] Threads      : {threads}\n'
        f'[+] Wordlist     : {wordlist_path}\n'
        f'[+] Status codes : {codes}\n'
        f'[+] User Agent   : {user_agent}\n'
        f'[+] Timeout      : {timeout}s\n'
        f'==============================================================='
    )


def generate_timestamped_line(content):
    return (
        f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} {content}'
    )


def generate_url_line(url, status):
    return f'/{url.split("/")[-1]}'
