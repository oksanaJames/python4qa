from urllib import request, parse
import requests

url = 'http://httpbin.org/post'

parms = {
    "comments": "11111111",
    "custemail": "test@gmail.com",
    "custname": "tttt",
    "custtel": "55555555555",
    "delivery": "",
    "size": "small",
    "topping": "bacon"
}

querystring = parse.urlencode(parms)
u = request.urlopen(url, querystring.encode('utf-8'))
resp = u.read().decode('utf-8')
print(resp)