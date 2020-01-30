from datetime import datetime


class Logger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def ruler(self):
        print('===============================================================', flush=True)

    def banner(self, url, threads, wordlist_path, codes, user_agent, timeout):
        newline = '\n'
        print(
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
            f'{"[+] Verbose      : True" + newline if self.verbose else ""}'
            f'==============================================================='
        )

    def timestamped_line(self, content):
        print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} {content}', flush=True)

    def response_line(self, response):
        path = response.url.split("/")[-1]
        if self.verbose:
            print(f'{"Found" if response.is_valid else "Missed"}: /{path} (Status: {response.status})', flush=True)
        elif response.is_valid:
            print(f'/{path} (Status: {response.status})', flush=True)
