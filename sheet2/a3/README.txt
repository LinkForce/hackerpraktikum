Before running the scripts, please run installDepencies.sh to install all dependencies needed by the scripts

Bank (Aufgabe 3)

In this exercise I found 3 diferent types of vulnerabilities.

The first one was XSS Injection. This vulnerability happens on every user input besides login and register forms.
This means, the settings, where you can change your first and last name, on the support questions, and on the message field of transactions. All those inputs were safe from SQL injection cause the database uses parameters on its procedures. To exploit this vulnerability, I wrote a script that creates a user, creates a card, and then transfer $1 to every other card available in the database (assuming cards always goes from 0 to mycard - 1 concat with 1337 and remaining zeros), and adds a script in the message that, when the victim checks his transaction page, it sends me more money in return. You can run it like:
	
	python xssteal.py 

After that just log in with any user already registered to the platform that has a card and go to the transactions page to see the script working.

To patch this vulnerability, I just sanitized every user input by using the functions strip_tags, addslashes and htmlspecialchars from php. 

You can see these edits in the files UserClass.php, card2card.php and support.php.

The second vulnerability was a Improper Access to the index/userlist resource on the system. This resource should be only acessible (I suppose) to a user authenticated as support. You can exploit this vulnerability simply requesting the url authenticated as any user. You can do that by running the script getusers.py like:

	python getusers.py

To patch this vulnerability, I add another verification along with the one that checks if the user is authenticated, that checks if the user is support.

You can see this edit in the file index.php.

And the last one was a Improper Data Request on the export function of the transaction page. If you manipulate a hidden field in the page, you can change the user id and request the transactions list of any user in the bank.
You can check this vulnerability by running the transactions.py script. It returns, in XML format, the list of transactions of the user of ID 1 (Usually support), that contains a flag for every transaction that the user made.
Run ths script like:
	
	python transactions.py

To patch this vulnerability, I made the code ignore this field and use the id from $_SESSION['userdata'] instead of getting it from $_REQUEST.

You can see this edit in the file card2card.php.

The patch file patches all those vulnerabilities. I generated it accordingly to the gitlab instructions, so it should be executed from / inside the docker with the command:

	patch -p1 -i bank.patch

And this fixes all the vulnerabilities that I discovered.