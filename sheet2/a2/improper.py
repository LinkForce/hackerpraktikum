import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

#form data for user registry
register_data = {
'first_name': 'N.', 
'last_name': 'NotObrian',
'city': '',
'gender': '',
'birthdayYear': '',
'face': '',
'motivation': '',
'tag':'',
'skill':'',
'style':'',
'jabber':'',
'email': 'man@ahmadinedschad.am',
'website':'',
'job':'',
'interests':'',
'aboutme':'',
'password': '12345678',
'passwordRepeat': '12345678'
}

#request to register on myspray
response = s.post(baseurl + 'register.html', data = register_data)

#regex to look for meta redirects
regex = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

match = regex.search(response.text)

while match: #loop for redirecting until logged in
    response = s.get(baseurl + match.groups()[0].strip())
    match = regex.search(response.text)

print response.text

#request received messages
response = s.get(baseurl + 'inbox.html')
print response.text

#request sent messages
response = s.get(baseurl + 'outbox.html')
print response.text
