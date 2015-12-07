from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus



url = 'https://api.shop.com/hello-world'
headers = {  'apikey':'l7xx175ed35d49844df29b26917291a11038'  }
request = Request(url, headers=headers)
request.get_method = lambda: 'GET' 
response_body = urlopen(request).read()
print response_body
