<html>
<head>
<title>Encode Software</title>
<link rel="stylesheet" href="encryptor.css"> 
</head>
<body>
<div class="menu">
<a href="<?PHP echo $_SERVER['PHP_SELF']; ?>">Home</a> - 
<a href="<?PHP echo $_SERVER['PHP_SELF'].'?op=record'; ?>">Record</a> -
<a href="<?PHP echo $_SERVER['PHP_SELF'].'?op=about'; ?>">About</a>
</div>
<div class="main">
<form action="<?PHP echo $_SERVER['PHP_SELF']; ?>" method="post">
<input type="text" name="input" size="67"><br / >
<input type="submit" value="New" name="op">
<input type="submit" value="Load" name="op">
<input type="submit" value="Encode" name="op">
<input type="submit" value="Decode" name="op">
<input type="submit" value="Clean" name="op">
</form>
</div>
<div class="display">
<?php
switch ($_REQUEST["op"]) {
    case "New":
        echo "There is <b>New</b> button.";
        break;
     
    case "Load":
        echo "There is <b>Load</b> button.";
        break;
     
    case "Encode":
        echo "There is <b>Encode</b> button. Your input is '{$_POST['input']}'.";
        break;
     
    case "Decode":
        echo "There is <b>Decode</b> button. Your input is '{$_POST['input']}'.";
        break;
     
    case "Clean":
        echo "There is <b>Clean</b> button.";
        break;
     
    case "record":
        echo "There is <b><i>Record</i></b> page.";
        break;
     
 case "about":
        echo "There is <b><i>About</i></b> page.";
        break;
     
    default:
        echo "something happened";    
}
?>
</div>
<div>
<div class="test">
<?php
	$last_line = system('python3 test.py', $retval);
	echo '<hr />Return value: ' . $retval;
?>
</div>
</body>
</html>