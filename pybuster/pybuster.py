#!/usr/bin/python3
import sys
import argparse
import queue
import requests
from threading import Thread
from output import generate_banner, generate_timestamped_line, generate_ruler, generate_url_line


class Response:
    def __init__(self, url):
        self.url = url
        self.status = None
        self.is_valid = False


def check_url(url, positive_codes):
    """
    Check the given URL for a response, store and return metadata
    """
    response = Response(url)
    try:
        res = requests.head(url)

        response.status = res.status_code
        if response.status in positive_codes:
            response.is_valid = True
    except Exception as e:
        print(f'ERROR: Timeout or unexpected response from {url}')
        response.is_valid = False

    return response


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


def work(q, base_url, positive_codes):
    """
    Thread worker function, processes entries from URL queue until empty
    """
    while not q.empty():
        word = q.get()
        url = base_url + '/' + word

        response = check_url(url, positive_codes)
        if response.is_valid:
            print(generate_url_line(url, response.status))

        q.task_done()


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(
        description='Web URI bruteforcing in Python', formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-u', '--url', type=str, required=True, help='The target URL')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to the wordlist')
    parser.add_argument('-s', '--statuscodes', type=str, default='200,204,301,302,307,401,403', help='Positive status codes')
    parser.add_argument('-a', '--useragent', type=str, default='pybuster/0.1', help='The User-Agent string to be used')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of concurrent threads')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP request timeout in seconds')
    args = parser.parse_args()

    base_url = args.url.rstrip('/')
    wordlist_path = args.wordlist
    positive_codes = [int(x) for x in args.statuscodes.split(',')]
    user_agent = args.useragent
    threads = args.threads
    timeout = args.timeout

    # Check that we can access the base URL before starting
    initial_response = check_url(base_url, positive_codes)
    if initial_response.is_valid:
        print(generate_banner(base_url, threads, wordlist_path, args.statuscodes, user_agent, timeout), flush=True)
        print(generate_timestamped_line('Starting pybuster'), flush=True)
        print(generate_ruler())

        url_queue = build_url_queue(wordlist_path)

        for i in range(threads):
            t = Thread(target=work, args=(url_queue, base_url, positive_codes))
            t.start()
        url_queue.join()

        print(generate_ruler())
        print(generate_timestamped_line('Finished'))
        print(generate_ruler())
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()