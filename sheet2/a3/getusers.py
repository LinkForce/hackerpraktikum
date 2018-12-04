import requests
import re
import json

s = requests.Session()

baseurl = 'http://10.0.23.24:7777/'

register_data = {
'username': 'haxx0r',
'password': '12345678'
}

#register
response = s.post(baseurl + 'register', data = register_data)

#login
response = s.post(baseurl + 'login', data = register_data)

#regex to look for meta redirects
regex = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

match = regex.search(response.text)

while match: #loop for redirecting until logged in
    response = s.get(baseurl + match.groups()[0].strip())
    match = regex.search(response.text)

#get userlist
response = s.get(baseurl + '/index/userlist')

print response.text