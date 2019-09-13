Malware Analysis (Aufgabe 2)

How does the app initially camouflage itself and what is its purpose?

The app pretends to be a Word Cloud generator based on your messages and contacts, and uses that to ask for permission to access your contacts,
your calendar, your SMS' and your files. Once the app get the permissions, it steals the contacts list from the user, save it to a file, delete
the contacts and creates a calendar event asking the user to pay bitcoins to get its contacts back. It also steals the users' SMS history, and
open a shell that allows the attacker to execute any desired command into the cellphone, and tries to use this connection to send the contacts 
and user list to the hacker.

How is the app's malicious routine structured?

Firs the app does various verifications to detect emulation and monitoring, looking for some system strings that says the app is running inside
emulators, checks the architecture, if there is any bluetooth adapter, some paths on the environment etc. If the apps pass all the verifications
and boot, it asks for the permissions and, when you click to generate the word cloud, it starts the WordCloudActivity. This activity make some 
anti monitoring verifications too, and after that starts the procedure of stealing contacts, saving it on a txt file base64-encoded, tries to 
send the information to the atacker and creates the calendar event asking for payment.

Can the app reverse the changes to the system? If so, how?

Yes it can. The malware is flawed because it leaves the original information on the users phone. It should send the info to the attacker and
after that delete the file, so that the user cannot recover the data without paying for it. So you just have to read the txt file with the 
base64 encoded contacts, decoded it and insert the contacts back. You can use the FixMalware.apk to revert the changes. I also included the 
source code inside the tar.gz file, maybe it is a little bloated because I wrote it with Android Studio.