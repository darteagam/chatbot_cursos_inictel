<?php

$consulta = $_POST['message'];

$nombre = "Iván Santos";

sleep(3);
//
//echo 'La respuesta esta en espera, disculpe la tardanza';

$command1 = "cd /var/www/html/chatbot_cursos_inictel/";
$command2 = "/var/www/html/chatbot_cursos_inictel/venv/bin/python -m backend.conv_manager.question_answering '" . $nombre . "' '" . $consulta."'";
$command_exec = $command1 . ' ; ' . $command2;
$fileName = trim(shell_exec($command_exec));
echo $fileName;

//echo $command_exec;
