import requests

r = requests.get('http://httpbin.org/get')

print r.content

print r

r = requests.post("http://httpbin.org/post")

print r.content
print r