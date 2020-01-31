import sys
from datetime import datetime
from tqdm import tqdm


class Logger:
    def __init__(self, verbose=False, no_status=False, quiet=False, expanded=False, include_length=False, output_file=None, add_slash=False):
        self.verbose = verbose
        self.no_status = no_status
        self.quiet = quiet
        self.expanded = expanded
        self.include_length = include_length
        self.add_slash = add_slash
        try:
            if output_file is not None:
                sys.stdout = open(output_file, 'w')
        except PermissionError:
            print(f'ERROR: Permission denied for output file "{output_file}"')
            sys.exit(1)

    def ruler(self):
        if self.quiet:
            return
        tqdm.write('===============================================================')

    def banner(self, url, threads, wordlist_path, codes, user_agent, timeout):
        if self.quiet:
            return
        newline = '\n'
        tqdm.write(
            f'===============================================================\n'
            f'Pybuster v0.1.0\n'
            f'by Leo Kontogiorgis (leo@konto.dev)\n'
            f'===============================================================\n'
            f'[+] Mode         : dir\n'
            f'[+] URL          : {url}\n'
            f'[+] Threads      : {threads}\n'
            f'[+] Wordlist     : {wordlist_path}\n'
            f'[+] Status codes : {codes}\n'
            f'[+] User Agent   : {user_agent}\n'
            f'[+] Timeout      : {timeout}s\n'
            f'{"[+] Expanded     : True" + newline if self.expanded else ""}'
            f'{"[+] No status    : True" + newline if self.no_status else ""}'
            f'{"[+] Quiet        : True" + newline if self.quiet else ""}'
            f'{"[+] Verbose      : True" + newline if self.verbose else ""}'
            f'==============================================================='
        )

    def timestamped_line(self, content):
        if self.quiet:
            return
        tqdm.write(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} {content}')

    def info_line(self, content):
        if self.quiet:
            return
        tqdm.write(f'[-] {content}')

    def response_line(self, response):
        if self.expanded:
            path = response.url
        else:
            if self.add_slash:
                path = '/' + response.url[:-1].split('/')[-1] + '/'
            else:
                path = '/' + response.url.split('/')[-1]

        if self.verbose:
            tqdm.write(
                f'{"Found" if response.is_valid else "Missed"}: {path}'
                f'{" (Status: " + str(response.status) + ")" if not self.no_status else ""}'
                f'{" [Size: " + str(response.length) + "]" if self.include_length else ""}'
            )
        elif response.is_valid:
            tqdm.write(
                f'{path}'
                f'{" (Status: " + str(response.status) + ")" if not self.no_status else ""}'
                f'{" [Size: " + str(response.length) + "]" if self.include_length else ""}'
            )
