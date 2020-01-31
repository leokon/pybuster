#!/usr/bin/python3
import sys
import argparse
import queue
from threading import Thread
from logger import Logger
from client import Client


class WorkerThread(Thread):
    def __init__(self, q, base_url, client, logger):
        Thread.__init__(self)
        self.q = q
        self.base_url = base_url
        self.client = client
        self.logger = logger

    def run(self):
        """
        Processes entries from URL queue until empty
        """
        while not self.q.empty():
            word = self.q.get()
            url = self.base_url + '/' + word

            response = self.client.check_url(url)
            self.logger.response_line(response)

            self.q.task_done()


def build_url_queue(wordlist_path):
    """
    Instantiates and populates the thread-friendly queue of URLs to be tested from the given wordlist filepath
    """
    q = queue.Queue(maxsize=0)
    try:
        with open(wordlist_path) as f:
            wordlist_lines = [line.strip() for line in f]
            [q.put(x) for x in wordlist_lines]
    except FileNotFoundError:
        print(f'ERROR: Wordlist file "{wordlist_path}" does not exist.')
        sys.exit(1)

    return q


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(
        description='Web URI bruteforcing in Python', formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-u', '--url', type=str, required=True, help='The target URL')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to the wordlist')
    parser.add_argument('-s', '--statuscodes', type=str, default='200,204,301,302,307,401,403', help='Positive status codes')
    parser.add_argument('-a', '--useragent', type=str, default='pybuster/0.1', help='The User-Agent string to be used')
    parser.add_argument('-r', '--followredirect', action='store_true', help='Follow redirects')
    parser.add_argument('-H', '--headers', action='append', default=None, help='Specify HTTP headers, -H \'Header1: val1\' -H \'Header2: val2\'')
    parser.add_argument('-c', '--cookies', action='append', default=None, help='Specify cookies to use, -c \'COOKIE=val1\' -c \'COOKIE2=val2\'')
    parser.add_argument('-U', '--username', type=str, help='Username for HTTP auth')
    parser.add_argument('-P', '--password', type=str, help='Password for HTTP auth')
    parser.add_argument('-k', '--insecuressl', action='store_true', help='Skip SSL certificate verification')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of concurrent threads')
    parser.add_argument('-o', '--output', type=str, help='Output file to write results to')
    parser.add_argument('-e', '--expanded', action='store_true', help='Expanded mode, print full URLs')
    parser.add_argument('-l', '--includelength', action='store_true', help='Include the length of the response body in the output')
    parser.add_argument('-n', '--nostatus', action='store_true', help='Don\'t print status codes')
    parser.add_argument('-q', '--quiet', action='store_true', help='Don\'t print anything but the results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP request timeout in seconds')
    args = parser.parse_args()

    base_url = args.url.rstrip('/')
    wordlist_path = args.wordlist
    positive_codes = [int(x) for x in args.statuscodes.split(',')]
    user_agent = args.useragent
    threads = args.threads
    timeout = args.timeout

    # Initialise logger
    logger = Logger(
        verbose=args.verbose,
        no_status=args.nostatus,
        quiet=args.quiet,
        expanded=args.expanded,
        include_length=args.includelength,
        output_file=args.output
    )

    # Initialise client
    client = Client(
        positive_codes,
        user_agent=user_agent,
        follow_redirect=args.followredirect,
        timeout=timeout,
        headers=args.headers,
        cookies=args.cookies,
        insecure_ssl=args.insecuressl,
        username=args.username,
        password=args.password
    )

    # Check that we can access the base URL before starting
    initial_response = client.check_url(base_url)
    if initial_response.is_valid:
        logger.banner(base_url, threads, wordlist_path, args.statuscodes, user_agent, timeout)
        logger.timestamped_line('Starting pybuster')
        logger.ruler()

        url_queue = build_url_queue(wordlist_path)

        for i in range(threads):
            worker = WorkerThread(url_queue, base_url, client, logger)
            worker.start()
        url_queue.join()

        logger.ruler()
        logger.timestamped_line('Finished')
        logger.ruler()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()