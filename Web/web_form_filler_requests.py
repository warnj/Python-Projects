import requests, json
from fake_useragent import UserAgent

# failed attempt to login to UW registration using requests - wants js to be enabled

# Fill in your details here to be posted to the login form.
# UA = UserAgent()
# chrm = UA.chrome

data = json.loads(open('../personal_data.json').read())

hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

payload = {
    'user': data["uw_username"],
    'pass': data["uw_password"],
    'create_ts': '1463631029',
    'creds_from_greq': '1',
    'first kiss': '	1463630174-6154',
    'five': 'GET',
    'flag': '0',
    'four': 'a5',
    'fr': 'NFR',
    'hostname': 'myuw.washington.edu',
    'nine': '1',
    'one': 'my.uw.edu',
    'pinit': '0',
    'pre_sess_tok': '-396147676',
    'referer': '(null)',
    'relay_url': 'https://my.uw.edu/PubCookie.reply',
    'reply': '1',
    'sess_re': '0',
    'seven': 'Lw==',
    'six': 'my.uw.edu',
    'submit': 'Log in',
    'three': '1',
    'two': 'MyUW'
}

# Use 'with' to ensure the session context is closed after use.
s = requests.Session()

p = s.get('https://weblogin.washington.edu/')
# print p.text
p = s.post('https://weblogin.washington.edu/', data=payload, headers=hdr)
# print the html returned or something more intelligent to see if it's a successful login page.
# print p.text

# An authorised request.
r = s.get('https://sdb.admin.uw.edu/students/uwnetid/register.asp')
print(r.text)

'''
r = requests.get('http://httpbin.org/get')

print r.content

print r

r = requests.post("http://httpbin.org/post", data={"hello"}, auth=('user', 'pass'))

print r.content
print r

#https://sdb.admin.uw.edu/students/uwnetid/register.asp'''
