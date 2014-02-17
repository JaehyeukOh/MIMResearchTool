<?php

// We're putting all our files in a directory called images.
$uploaddir = './text/';

// The posted data, for reference
try {
	$file = $_POST['value'];
	$name = $_POST['name'];
} catch(Exception $e)
{
	$file = Null;
	$name = Null;
}

// Get the mime
$getMime = explode('.', $name);
$mime = end($getMime);

// Separate out the data
$data = explode(',', $file);

// Encode it correctly
$encodedData = str_replace(' ','+',$data[1]);
$decodedData = base64_decode($encodedData);

// You can use the name given, or create a random name.
// We will create a random name!

$randomName = substr_replace(sha1(microtime(true)), '', 12);
$randomFileName = $randomName.'.'.$mime;

if(file_put_contents($uploaddir.$randomFileName, $decodedData)) {
	$ret = exec('python AnonymousHandler.py '.$uploaddir.' '.$randomFileName, $ret_array, $ret_value);
	
	try {
		$some_list_file = $uploaddir.'out_'.$randomFileName;
		
		$some_list_fp = fopen($some_list_file, "r") or exit("Error Occurred (변환 가능한 파일 형식이 아닙니다.)!");
		
		while (!feof($some_list_fp)) {
				echo fgets($some_list_fp) . "<br/>";
		}   
		
		fclose($some_list_fp);	
		unlink($some_list_file);	
	} catch (Exception $e)
	{
		echo 'Caught exception: ',  $e->getMessage(), "\n";
	}
}
else {
	// Show an error message should something go wrong.
	echo "Something went wrong. Check that the file isn't corrupted";
}

?>