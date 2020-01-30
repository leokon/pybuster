from datetime import datetime


class Logger:
    def __init__(self, verbose=False, no_status=False, quiet=False):
        self.verbose = verbose
        self.no_status = no_status
        self.quiet = quiet

    def ruler(self):
        if self.quiet:
            return
        print('===============================================================', flush=True)

    def banner(self, url, threads, wordlist_path, codes, user_agent, timeout):
        if self.quiet:
            return
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
            f'===============================================================',
            flush=True
        )

    def timestamped_line(self, content):
        if self.quiet:
            return
        print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} {content}', flush=True)

    def response_line(self, response):
        path = response.url.split("/")[-1]
        if self.verbose:
            print(
                f'{"Found" if response.is_valid else "Missed"}: /{path} '
                f'{"(Status: " + str(response.status) + ")" if not self.no_status else ""}',
                flush=True
            )
        elif response.is_valid:
            print(
                f'/{path} '
                f'{"(Status: " + str(response.status) + ")" if not self.no_status else ""}',
                flush=True
            )
