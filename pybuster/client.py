import sys
import requests
from requests.auth import HTTPBasicAuth


class Response:
    def __init__(self, url):
        self.url = url
        self.status = None
        self.length = None
        self.is_valid = False


class Client:
    def __init__(self, positive_status_codes, user_agent='Pybuster/0.1', timeout=10, follow_redirect=False,
                 headers=None, cookies=None, insecure_ssl=False, username=None, password=None):
        self.positive_status_codes = positive_status_codes
        self.timeout = timeout
        self.follow_redirect = follow_redirect
        self.headers = self.parse_headers(headers, user_agent)
        self.cookies = self.parse_cookies(cookies)
        self.insecure_ssl = insecure_ssl
        self.username = username
        self.password = password

    def check_url(self, url):
        """
        Make a request to the given URL and analyse the response, returning a Response object
        """
        response = Response(url)
        try:
            if self.username is not None and self.password is not None:
                auth = HTTPBasicAuth(self.username, self.password)
            else:
                auth = None

            res = requests.get(
                url,
                timeout=self.timeout,
                headers=self.headers,
                cookies=self.cookies,
                allow_redirects=self.follow_redirect,
                auth=auth,
                verify=self.insecure_ssl
            )

            response.status = res.status_code
            if response.status in self.positive_status_codes:
                response.is_valid = True

            response.length = len(res.content)
        except requests.exceptions.Timeout:
            print(f'ERROR: Request to {url} timed out.')
            response.is_valid = False
        except Exception as e:
            print(f'ERROR: Timeout or unexpected response from {url}')
            response.is_valid = False

        return response

    def parse_headers(self, headers, user_agent):
        """
        Generate header dict from a list of strings
        """
        if headers is not None:
            try:
                result = {header.split(':')[0].strip():header.split(':')[1].strip() for header in headers}
            except Exception:
                print(f'Invalid headers {str(headers)}')
                sys.exit(1)
            result['User-Agent'] = user_agent
            return result
        else:
            return {'User-Agent': user_agent}

    def parse_cookies(self, cookies):
        if cookies is not None:
            try:
                return {cookie.split('=')[0].strip():cookie.split('=')[1].strip() for cookie in cookies}
            except Exception:
                print(f'Invalid cookies {str(cookies)}')
                sys.exit(1)
        else:
            return {}
