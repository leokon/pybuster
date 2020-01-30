import requests


class Response:
    def __init__(self, url):
        self.url = url
        self.status = None
        self.length = None
        self.is_valid = False


class Client:
    def __init__(self, positive_status_codes, user_agent='Pybuster/0.1', follow_redirect=False, headers=None):
        self.positive_status_codes = positive_status_codes
        self.follow_redirect = follow_redirect
        self.headers = self.generate_headers(headers, user_agent)

    def check_url(self, url):
        """
        Make a request to the given URL and analyse the response, returning a Response object
        """
        response = Response(url)
        try:
            res = requests.get(url, headers=self.headers, allow_redirects=self.follow_redirect)

            response.status = res.status_code
            if response.status in self.positive_status_codes:
                response.is_valid = True

            response.length = len(res.content)
        except Exception as e:
            print(f'ERROR: Timeout or unexpected response from {url}')
            response.is_valid = False

        return response

    def generate_headers(self, headers, user_agent):
        """
        Generate header dict from a list of strings
        """
        if headers is not None:
            result = {header.split(':')[0].strip():header.split(':')[1].strip() for header in headers}
            result['User-Agent'] = user_agent
            return result
        else:
            return {'User-Agent': user_agent}
