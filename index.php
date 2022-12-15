<!DOCTYPE html>

<html lang="en" class="h-100">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatBot</title>
        <link rel="stylesheet" href="assets/css/bootstrap.min.css"/>
        <link rel="stylesheet" href="assets/css/styles.css"/>
        <script src="https://kit.fontawesome.com/cbc2ce1b81.js" crossorigin="anonymous"></script>

    </head>
    <body class="d-flex flex-column h-100">

        <!--inicio del chatbot-->

        <div class="chat-screen">
            <!-- Cabecera del chat -->
            <div class="chat-header">
                <div class="chat-header-title">
                    ¿Chateamos? - Estamos en línea
                </div>
                <div class="chat-header-option hide">
                    <span class="dropdown">
                        <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-ellipsis-h"></i>
                        </a>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuLink" style="font-size: 14px">
                            <a class="dropdown-item py-2" href="#">
                                <i class="far fa-file-alt"></i> 
                                Enviar Transcripción
                            </a>
                            <a class="dropdown-item py-2 end-chat" href="#">
                                <i class="fas fa-power-off"></i> 
                                Finalizar Chat
                            </a>
                        </div>
                    </span>
                </div>
            </div>
            <!-- Cuerpo: nombres y email -->
            <div class="chat-mail">
                <div class="row">
                    <div class="col-md-12 text-center mb-2">
                        <h6 class="mb-3">Hola! Complete el formulario para empezar a chatear!!!.</h6>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-4">
                            <input type="text" class="form-control" id="txtNameChat" placeholder="Ingrese su nombre" value="Ivan Gavino Leon" required="">
                        </div>
                        <div class="mb-4">
                            <input type="email" class="form-control" id="txtEmailChat" placeholder="Ingrese su email" value="ivangavino@gmail.com" required="">
                        </div>
                        <div class="mb-4">
                            <input type="text" class="form-control" id="txtSelected" placeholder="Ingrese su número de celular" value="987654321" required="">
                        </div>
                    </div>
                    <div class="col-md-12">
                        <button class="btn btn-primary btn-block boton1 ">Iniciar Chat</button>
                    </div>
                    <div class="col-md-12">
                        <p class="text-center text-danger mt-3" style="font-style: oblique; font-size: 12px" id="mensaje"></p>
                        <div class="powered-by" >Desarrollado por la Dirección de Investigación y Desarrollo Tecnológico de INICTEL-UNI</div>
                    </div>
                </div>
            </div>
            <!-- Cuerpo del chat -->
            <div class="chat-body hide">
                <div class="chat-start" id="hours">Lunes 19, 20:30</div>
                <div class="start" style="height: 1px; width: 300px"></div>
            </div>
            <!-- Input del chat -->
            <div class="chat-input hide">
                <form action="#" method="POST" id="chat-form">
                    <input type="text"  name="message" id="consultaChat" placeholder="Ingrese su consulta ..." autofocus="" required="">
                    <div class="input-action-icon">
                        <button id="send-chat" type="submit" class="btn" >
                            <i class="fas fa-paper-plane send-message"></i>
                        </button>
                    </div>
                </form>
            </div>
            <!-- Final de session del chat -->
            <div class="chat-session-end hide">
                <h5>Esta sesión de chat ha terminado</h5>
                <p>Gracias por chatear con nosotros, Si usted puede tomar un minuto y calificar este chat:</p>
                <div class="rate-me">
                    <div class="rate-bubble great">
                        <span class="class">
                            <i class="far fa-thumbs-up" style="color: #fff"></i>
                        </span>
                        Bien!
                    </div>
                    <div class="rate-bubble bad">
                        <span class="class">
                            <i class="far fa-thumbs-down" style="color: #fff"></i>
                        </span>
                        Mal!
                    </div>
                </div>
                <a class="transcript-chat" href="#">Necesita mas información?</a>
                <div class="powered-by" >Desarrollado por la Dirección de Investigación y Desarrollo Tecnológico de INICTEL-UNI</div>

            </div>
        </div>
        <div class="chat-bot-icon">
            <i class="far fa-comment  animate" style="margin-left: -5px"></i>
            <i class="fas fa-times "></i>
        </div>
        <!--Fin del chatbot-->
        <header>
            <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
                <div class="container">
                    <a class="navbar-brand" href="#">INICTEL - UNI</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarCollapse">
                        <ul class="navbar-nav mb-2 mb-md-0 ms-auto">
                            <li class="nav-item active"><a class="nav-link" href="#">Inicio</a></li>
                            <li class="nav-item"><a class="nav-link" href="#">Cursos</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
        <main class="flex-shrink-0 mt-5" style="border: 1px solid #fff">
            <div class="container">
                <h1 class="mt-5 text-center mb-3">Dirección de Capacitación y Transferencia Tecnológica</h1>
                <p class="lead" style="text-align: justify">
                    La Dirección de Capacitación y Transferencia Tecnológica tiene como objetivo promover, desarrollar supervisar y controlar las acciones de Capacitación en el área de telecomunicaciones, ingeniería de redes y networking tendientes a habilitar, especializar, y perfeccionar recursos humanos encargados de dirigir o ejecutar los servicios de telecomunicaciones, administrar redes corporativas y desarrollar y gestionar redes telemáticas, a través de los Programas de Especialización.
                </p>
                <p><a class="btn btn-primary btn-lg" href="http://aplica.inictel-uni.edu.pe:8080/cursos/home?codigoModalidad=1">Mas información</a></p>

            </div>
        </main>
        <footer class="footer mt-auto py-3 bg-light text-center">
            <div class="container">
                <span class="text-muted">@Copyright - Instituto Nacional de Investigación y 
                    Capacitación de Telecomunicaciones de la Universidad Nacional 
                    de Ingeniería.</span>
            </div>
        </footer>

        <script src="assets/js/jquery-3.6.0.min.js" type="text/javascript"></script>
        <script src="assets/js/popper.min.js" type="text/javascript"></script>
        <script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
        <script src="assets/js/clock.js" type="text/javascript"></script>
        <script src="assets/js/index.js" type="text/javascript"></script>







    </body>
</html>
