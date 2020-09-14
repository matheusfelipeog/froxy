<p align="center">
    <img src="https://img.shields.io/github/license/matheusfelipeog/froxy?color=black&style=for-the-badge" alt="License" />
</p>

<h1 align="center">
    <img src="./assets/froxy.png" alt="Froxy logo" width="500px" /><br />
    Hide your IP with free proxies
</h1>


## Index

- [The goal](#the-goal)
- [How it works?](#how-it-works)
   - [Why are you using this API?](#why-are-you-using-this-api)
- [Demo](#demo)
   - [Warning](#-warning-)
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


## License

This project is using the MIT license, see in [MIT LICENSE](./LICENSE).

For more information on the API used, visit [clarketm/proxy-list](https://github.com/clarketm/proxy-list).
