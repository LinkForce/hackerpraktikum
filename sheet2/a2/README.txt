Before running the scripts, please run installDepencies.sh to install all dependencies needed by the scripts

Social Networks (Aufgabe 2)

1. SQL Injection

To solve this exercise, just run the sqlinjection.py script to login on myspray as Hanni Ball.
This exercise is solved by injecting sql into the login form to make the login look for user's first name,
instead of login and password as expected.

Additionally, you can pipe the output on w3m to have a pretty printed html on the terminal.
Example:

	python sqlinjection.py | w3m -dump -T text/html

2. Improper Authentication

To solve this exercise, just run the improper.py script to get N. O’Brian's information.
This exercise is solved by creating a new user that has the same name and email that N. O’Brian,
as the application does not check for duplicity and the critical codes provided uses those information
to load the user message box and sprayed by list.

Additionally, you can pipe the output on w3m to have a pretty printed html on the terminal.
Example:

	python improper.py | w3m -dump -T text/html

3. Unrestricted File Upload

To solve this exercise, just run the fileupload.py to create a new user and upload a php shell into user's gallery.
This exercise is solved by simply uploading the php file, as the application does not do any checking on the file
being upload.

Example:
	python fileupload.py

4. Cross-Site Scripting

The website contais 3 entry points for stored XSS injection:
	The user's profile "About" field.
	The user's loogbok
	The user's private message field

To exploit this vulnerabillity, first run the cookiesteal.py script to create a user with a cookie stealing script 
on his profile page, on the about field. The script just get the cookies from the document.cookies variable.

Example:
	python cookiesteal.py

After that, you have to login in the system via a browser with any user and access Cookie Stealer's profile page (usually clicking on latest member works).
You can use, for example, the user from fileupload.py to make it easier.

After looking at Cookie Stealer's page, the user will have sent a message with it's own cookie to Cookie Stealer's inbox. You can check his inbox by running the checkinbox.py script.

Additionally, you can pipe the output on w3c to have a pretty printed html on the terminal.
Example:

	python checkinbox.py | w3m -dump -T text/html

Finally, to login using the cookie stolen from the user, you can run loginwithcookies.py with the cookie as an argument.

Additionally, you can pipe the output on w3m to have a pretty printed html on the terminal.
Example:

	python loginwithcookies.py STOLEN_COOKIES | w3m -dump -T text/html

5. Cross-Site Request Forgery

To solve this exercise, just access the goodpage.html in a browser that is already logged in some user at MySpray.
The page should automatically send a message to Hanni Ball in the name of the logged user, via an post inside an Iframe, making that the user browser does not refresh to send the message.

6. XSS Worm

You can find the worm in human readable form inside the worm.js file.
To test the worm, just run the worm.py script to create a user with the worm in it's own logbook. After that, just 
log in with any user and access the infected profile page (usually clicking on latest member works).
You can use, for example, the user from fileupload.py to make it easier.

After that the worm should have been spread to the user's logbook and all of its friends.