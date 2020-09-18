<p align="center">
    <img src="https://img.shields.io/github/license/matheusfelipeog/froxy?color=black&style=for-the-badge" alt="License" />
</p>

<h1 align="center">
    <img src="https://github.com/matheusfelipeog/froxy/blob/master/assets/froxy.png" alt="Froxy logo" width="500px" /><br />
    Hide your IP with free proxies
</h1>


## Index

- [The goal](#the-goal)
- [How it works?](#how-it-works)
   - [Why are you using this API?](#why-are-you-using-this-api)
- [Install](#install)
- [Demo](#demo)
   - [Warning](#-warning-)
- [Documentation](#doc)
- [License](#license)


## The goal

This project aims to provide an interface for filter and using free proxies in your web scraping and web crawler projects with Python and [requests module](https://github.com/psf/requests).


## How it works?

Froxy uses the API available at **[Proxy List](https://github.com/clarketm/proxy-list)** and runs a filter to obtain only proxies and their information. Then it provides an interface to filter and use the filtered proxies.

### Why are you using this API?

- It free.
- No query limit.
- It has a variety of types of proxies.
- It has an interesting amount of proxies.
- It is updated daily.

Thank you for maintaining and making this API available [@clarketm](https://github.com/clarketm) ❤


## Install

install using pip:

```bash
$ pip install froxy
```

then, see the **[demo](#demo)** or **[documentation](#doc)** for more information.


## Demo

This is a demo use to get proxies with a filter:

```python
from froxy import Froxy

froxy = Froxy()

for proxy in froxy.https(): # Get proxies with protocol https
    print(proxy)

# Output
['125.17.80.226', '8080', ['IN', 'H', 'S', '+']]  
['31.204.180.44', '53281', ['RU', 'H', 'S', '-']] 
['213.108.173.247', '8080', ['RU', 'N', 'S', '-']]
['109.169.151.131', '8080', ['RU', 'N', 'S', '+']]
['149.129.240.8', '8080', ['SG', 'N', 'S', '-']],
[...]
```

This a demo use with requests module:

```python
import requests

from froxy import Froxy

froxy = Froxy()
ip, port, *_ = froxy.http()[0] # Get first proxy (IP and PORT)

proxies = {
    "http": f'{ip}:{port}',
    "https": f'{ip}:{port}'
}

r = requests.get('https://httpbin.org/ip', proxies=proxies)
print(f'Response: {r.json()}')

# Output
Response: {'origin': '103.250.69.233'}
```

 ### ⚠ Warning ⚠
 
 **Not all proxies work, so try to use only those that work use `try...except` as a "filter"**
 
 Basic example:
 ```python
import requests

from froxy import Froxy

froxy = Froxy()

for proxy in froxy.http():
    ip, port, *_ = proxy
    
    proxies = {
        "http": f'{ip}:{port}',
        "https": f'{ip}:{port}'
    }
    
    try:
        r = requests.get('https://httpbin.org/ip', proxies=proxies)
        print(f'Response: {r.json()}')
        
    except Exception:
        print('Fail, next...')
        continue
        
# output
Response: {'origin': '103.250.69.233'}
Fail, next...
Fail, next...
Fail, next...
Fail, next...
Response: {'origin': '212.32.213.170'}
...
```


# Doc

This is return of Froxy class using `help(Froxy)`:
```bash
class Froxy(builtins.object)
 |  A class for manipulating and filtering proxies.
 |
 |  All public method returns are made up of a list of lists in the following structure:
 |
 |  [
 |      [ip_adress, port, [country_code, anonymity, http_or_https, google_passed]],
 |      ...
 |  ]
 |
 |  Example:
 |
 |  [
 |      ['189.6.191.184', '8080', ['BR', 'N', 'S', '+']],
 |      ...
 |  ]
 |
 |  ___________________________________________________________________
 |
 |  Location of Froxy project: https://github.com/matheusfelipeog/froxy
 |
 |  Location of API used: https://github.com/clarketm/proxy-list
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |      Initialize storage attributes and start method to save to storage.
 |
 |      Public Attribute:
 |
 |      `storage: list` - Data storage and manipulation object
 |
 |  anonymity(self, *flags: tuple) -> list
 |      Filter proxies by anonymity level.
 |      
 |      Keyword arguments:
 |
 |      `flags: tuple` - Filter flags of selected anonymity level.
 |
 |      Anonymity levels:
 |          - Flags:
 |              - N = No anonymity
 |              - A = Anonymity
 |              - H = High anonymity
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.anonymity('A', 'H')
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['RS', 'H', 'S!', '-'],
 |          ['254.254.254.254', '8058', ['US', 'A', 'S!', '+'],
 |          ...
 |      ]
 |      ```
 |
 |  country(self, *flags: tuple) -> list
 |      Filter proxies for country.
 |
 |      Use the country code to filter proxies.
 |      
 |      Keyword arguments:
 |
 |      `flags: tuple` - Filter flags of selected countries.
 |
 |      Code example:
 |          BR = Brazil
 |          US = United States of America
 |          EG = Egypt
 |          (...)
 |
 |      See all codes at: [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.country('RS', 'US')
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['RS', 'N', 'S!', '-'],
 |          ['254.254.254.254', '8058', ['US', 'N', 'S!', '+'],
 |          ...
 |      ]
 |      ```
 |
 |  get(self, country: list = [], anonymity: list = [], protocol: list = [], google_passed: list = []) -> list
 |      Use multiple proxy filters or get all proxies if the filter arguments are empty.
 |
 |      Keyword arguments:
 |
 |      `country: list` - Number and List of flags of selected countries.
 |          - More info at: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
 |      
 |      `anonymity: list` - Number and List of flags of selected anonymity level. (N, A or H).
 |
 |      `protocol: list` - Number and Selected protocol (http or https).
 |
 |      `google_passed: list` - Number and Filter flags of google passed. (- or +).
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.get(
 |              country=[1, 'US', 'BR'],
 |              anonymity=[2, 'H'],
 |              protocol=[2, 'https'],
 |              google_passed=[1, '+']
 |          )
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['US', 'H', 'S!', '+'],
 |          ['254.254.254.254', '8058', ['BR', 'A', 'S', '+'],
 |          ['254.254.254.253', '6000', ['TT', 'H', '', '-'],
 |          ['254.254.254.252', '4058', ['BR', 'H', '!', '-'],
 |          ['255.255.255.251', '3000', ['RS', 'H', 'S', '-'],
 |          ['254.254.254.250', '7058', ['ZZ', 'H', 'S!', '-'],
 |          ['254.254.254.250', '7058', ['YY', 'N', '', '+']
 |      ]
 |      ```
 |
 |  google(self, flag: str, *args, **kwargs) -> list
 |      Filter proxies by google passed.
 |
 |      Keyword arguments:
 |
 |      `flags: tuple` - Filter flags of google passed.
 |          - (+) = Yes
 |          - (-) = No
 |
 |      A Google proxy (also known as the google-passed proxy)
 |      is an HTTP proxy which has the following two features:
 |          - 1. It must support searching on Google and a Google
 |               proxy should support HTTPS/SSL;
 |          - 2. Google must not block it.
 |
 |          More info at: https://free-proxy-list.net/blog/google-proxies-dead
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.google('+')
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['AA', 'H', 'S!', '+'],
 |          ['254.254.254.254', '8058', ['YY', 'N', '', '+'],
 |          ...
 |      ]
 |      ```
 |
 |  http(self, *args, **kwargs) -> list
 |      Filter proxies by http protocol.
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.http()
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['AA', 'H', '!', '-'],
 |          ['254.254.254.254', '8058', ['ZZ', 'A', '', '+'],
 |          ...
 |      ]
 |      ```
 |
 |  https(self, *args, **kwargs) -> list
 |      Filter proxies by https protocol.
 |
 |      Usage:
 |      ```
 |      >>> from froxy import Froxy
 |      >>> froxy = Froxy()
 |      >>> froxy.https()
 |      # Example output
 |      [
 |          ['255.255.255.255', '3000', ['AA', 'H', 'S!', '-'],
 |          ['254.254.254.254', '8058', ['ZZ', 'A', 'S', '+'],
 |          ...
 |      ]
 |      ```
 |
 |  ----------------------------------------------------------------------
```


## License

This project is using the MIT license, see in [MIT LICENSE](./LICENSE).

For more information on the API used, visit [clarketm/proxy-list](https://github.com/clarketm/proxy-list).
