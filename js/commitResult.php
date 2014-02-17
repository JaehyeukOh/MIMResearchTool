<?php

$con = mysql_connect('localhost', 'USERNAME', 'PASSWORD');  
if (!$con)
{
	die('Could not connect: ' . mysql_error());
}

mysql_query("set character_set_connection=utf8;");
mysql_query("set character_set_server=utf8;");
mysql_query("set character_set_client=utf8;");
mysql_query("set character_set_results=utf8;");
mysql_query("set character_set_database=utf8;");

mysql_select_db('fddb', $con);  

try {
	clickLog($con);
} catch(Exception $e)
{
	echo $e;
}

mysql_close($con);	


function clickLog($con)
{
	$name = $_POST['key'];
	$data = $_POST['data'];
	$currentDate = date('Y-m-d H:i:s');
	
	# save data
}

?>