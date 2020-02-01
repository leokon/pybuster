# Pybuster

Pybuster is a multi-threaded tool for brute-forcing paths on web servers.

It is an  extended reimplementation of dirbuster/dirb in Python 3, with heavy inspiration taken from [gobuster](https://github.com/OJ/gobuster).

![](demo.gif)

## Installation
#### Using pip
`pip3 install pybuster`

#### From source
```
git clone https://github.com/leokon/pybuster.git
cd pybuster
pip3 install .
```

## Usage
Run with default options:
```
pybuster -u https://pypi.org -w /wordlists/common.txt

===============================================================
Pybuster v0.1.0
by Leo Kontogiorgis (leo@konto.dev)
===============================================================
[+] Mode         : dir
[+] URL          : https://pypi.org
[+] Threads      : 10
[+] Wordlist     : /wordlists/common.txt
[+] Status codes : 200,204,301,302,307,401,403
[+] User Agent   : pybuster/0.1.0
[+] Timeout      : 10s
===============================================================
2020/01/31 13:52:43 Starting pybuster
===============================================================
/ (Status: 200)
/admin (Status: 301)
/legacy (Status: 301)
/packages (Status: 301)
/robots.txt (Status: 200)
/search (Status: 301)
/sitemap.xml (Status: 200)
/sponsors (Status: 301)
===============================================================
2020/01/31 13:54:50 Finished
===============================================================
```

Run with verbose output and content length:
```
pybuster -u https://pypi.org -w /wordlists/short.txt -v -l

===============================================================
Pybuster v0.1.0
by Leo Kontogiorgis (leo@konto.dev)
===============================================================
[+] Mode         : dir
[+] URL          : https://pypi.org
[+] Threads      : 10
[+] Wordlist     : /wordlists/common.txt
[+] Status codes : 200,204,301,302,307,401,403
[+] User Agent   : pybuster/0.1.0
[+] Timeout      : 10s
[+] Verbose      : True
===============================================================
2020/01/31 13:56:41 Starting pybuster
===============================================================
Found: / (Status: 200) [Size: 21187]
Found: /admin (Status: 301) [Size: 204]
Missed: /afakepath (Status: 404) [Size: 4565]
Found: /help (Status: 301) [Size: 203]
Found: /legacy (Status: 301) [Size: 205]
Found: /packages (Status: 301) [Size: 207]
Missed: /packages2 (Status: 404) [Size: 4565]
Found: /robots.txt (Status: 200) [Size: 181]
Found: /sitemap.xml (Status: 200) [Size: 2124]
Found: /sponsors (Status: 301) [Size: 207]
===============================================================
2020/01/31 13:56:51 Finished
===============================================================
```

Run in quiet mode (useful for piping to grep):
```
pybuster -u https://pypi.org -w /wordlists/common.txt -q -n -e
https://pypi.org/
https://pypi.org/admin
https://pypi.org/help
https://pypi.org/legacy
https://pypi.org/packages
https://pypi.org/robots.txt
https://pypi.org/sitemap.xml
https://pypi.org/sponsors
```

#### Options
```
Usage:
  pybuster [args]

-h, --help            show this help message and exit
-u URL, --url URL     The target URL
-w, --wordlist        Path to the wordlist
-s, --statuscodes     Positive status codes (default: 200,204,301,302,307,401,403)
-a, --useragent       The User-Agent string to be used (default: pybuster/0.1.0)
-r, --followredirect  Follow redirects
-H, --headers         Specify HTTP headers, -H 'Header1: val1' -H 'Header2: val2'
-c, --cookies         Specify cookies to use, -c 'COOKIE=val1' -c 'COOKIE2=val2'
-U, --username        Username for HTTP auth
-P, --password        Password for HTTP auth
-p, --proxy           Proxy to use for requests [http(s)://host:port]
-k, --insecuressl     Skip SSL certificate verification
-f, --addslash        Append / to each request
-x, --extension       File extension to search for
-t, --threads         Number of concurrent threads (default: 10)
-o, --output          Output file to write results to
-e, --expanded        Expanded mode, print full URLs
-l, --includelength   Include the length of the response body in the output
-n, --nostatus        Don't print status codes
-q, --quiet           Don't print anything but the results
-v, --verbose         Verbose output
--ignorewildcard      Continue operation as normal when wildcard returns a positive status code
--timeout             HTTP request timeout in seconds (default: 10)
```

## Planned features
* Crawl pages looking for paths to add to the queue
* "Grep mode", specify positive results based on a regex instead of a HTTP status code