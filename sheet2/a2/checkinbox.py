import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

#you can login with a get with querystring parameters with email and password
response = s.get(baseurl + 'login.html?email=lost@cookies.com&password=12345678&login=Login')

#regex to look for meta redirects
regex = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

match = regex.search(response.text)

while match: #loop for redirecting until logged in
    response = s.get(baseurl + match.groups()[0].strip())
    match = regex.search(response.text)

#requesting user inbox to check for stolen cookies
response = s.get(baseurl + 'inbox.html')

print response.text