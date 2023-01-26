<?php

$consulta = $_POST['message'];

$nombre = "Ivan Santos";

sleep(3);
//
//echo 'La respuesta esta en espera, disculpe la tardanza';

//$command1 = "cd /var/www/html/chatbot_cursos_inictel/";
//$command2 = "/var/www/html/chatbot_cursos_inictel/venv/bin/python -m backend.conv_manager.question_answering '" . $nombre . "' '" . $consulta."'";
//$command_exec = $command1 . ' ; ' . $command2;
//$fileName = trim(shell_exec($command_exec));
//echo $fileName;

//echo $command_exec;


$url = 'http://127.0.0.1:8000/chatbot/'; 
$data = array("input" => $consulta, "user" =>$nombre);
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($curl, CURLOPT_PORT, 8000); #OR without this option
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // For HTTPS
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); // For HTTPS
curl_setopt($curl, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json', 'server:uvicorn'
]);
$response = curl_exec($curl);
$respuesta = json_decode($response,true);
echo $respuesta["output"];
//var_dump($respuesta);
//curl_close($curl);
