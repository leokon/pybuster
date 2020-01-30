import requests


class Response:
    def __init__(self, url):
        self.url = url
        self.status = None
        self.length = None
        self.is_valid = False


class Client:
    def __init__(self, positive_status_codes):
        self.positive_status_codes = positive_status_codes

    def check_url(self, url):
        """
        Make a request to the given URL and analyse the response, returning a Response object
        """
        response = Response(url)
        try:
            res = requests.get(url)

            response.status = res.status_code
            if response.status in self.positive_status_codes:
                response.is_valid = True

            response.length = len(res.content)
        except Exception as e:
            print(f'ERROR: Timeout or unexpected response from {url}')
            response.is_valid = False

        return response
