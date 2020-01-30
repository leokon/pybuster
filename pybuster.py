#!/usr/bin/python3
import argparse
import requests
from helpers.output import generate_banner


def check_url(url, positive_codes):
    """
    Check that the given URL exists and is accessible.
    """
    try:
        response = requests.get(url)
        if response.status_code in positive_codes:
            return True
    except Exception as e:
        print("Timeout or unexpected response from " + url)
        return False


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

    base_url = args.url
    wordlist_path = args.wordlist
    positive_codes = [int(x) for x in args.statuscodes.split(',')]
    user_agent = args.useragent
    threads = args.threads
    timeout = args.timeout

    # Check that we can access the base URL
    if check_url(base_url, positive_codes):
        print(generate_banner(base_url, threads, wordlist_path, args.statuscodes, user_agent, timeout))


if __name__ == "__main__":
    main()