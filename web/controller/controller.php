<?php

$nombres = $_POST['name'];
$email = $_POST['email'];
$telefono = $_POST['phone'];

$nombre_session = explode(" ", $nombres);
$data_interfaz = $nombre_session[0];

session_start();
//
$_SESSION["nombres"] = $data_interfaz;
//$_SESSION["email"] = $email;
//$_SESSION["celular"] = $telefono;

//echo $nombre_session;
echo ''.$_SESSION["nombres"];

