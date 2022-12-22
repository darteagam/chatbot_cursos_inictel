

jQuery(document).ready(function () {
//$(document).ready(function () {
    $(".chat-bot-icon").click(function (e) {
        $(this).children("i").toggleClass("animate");
        $(".chat-screen").toggleClass("show-chat");
    });

    $(".chat-mail .boton1").click(function () {
        var ExRegEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/;
        var ExRegName = /^[a-zA-ZÀ-ÿ\s]{12,80}$/;
        var name = document.getElementById('txtNameChat').value;
        var email = document.getElementById('txtEmailChat').value;
        var celular = document.getElementById('txtSelected').value;
        var messaje = document.getElementById('mensaje');

        if (!ExRegName.test(name)) {
            messaje.innerHTML = "Ingrese nombres y apellidos correctamente!!";
        } else if (!ExRegEmail.test(email)) {
            messaje.innerHTML = "Ingrese una dirección de correo electrónico válido.";
        } else {
            $.ajax({
                url: "web/controller/controller.php",
                type: 'POST',
                data: {
                    name: name,
                    email: email,
                    phone: celular
                },
                success: function (result) {
                    document.getElementById('datos_usuario').textContent = result;
                }
            });
        }

        $('.chat-mail').addClass('hide');
        $('.chat-body').removeClass('hide');
        $('.chat-input').removeClass('hide');
        $('.chat-header-option').removeClass('hide');

        $('.chat-body').append('<div class="chat-package"><div class="spinner last-spining"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div><div class="chat-bubble tu hide last-message">Bienvenido a nuestro sitio <span id="datos_usuario"></span>, si necesita información respecto a los cursos que se dicta en la institución, escriba su consulta que estamos en linea y listos para ayudar.<span class="message-time">' + getHoraActual() + '</span></div><div class="clear"></div></div>');

        setTimeout(function () {
            $('.last-spining').hide(400, function () {
                $('.last-message').fadeIn('fast');
                $('.last-spining').removeClass('last-spining');
                $('.last-message').removeClass('hide');
                $('.start').addClass('hide');
            });
        }, 1000);


    });


//codigo para formulario

    $("#chat-form").submit(function (e) {
        e.preventDefault();

        var consulta = document.getElementById('consultaChat').value;
        var mensaje = '<div class="chat-package"><div class="spinner last-spining"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div><div class="chat-bubble el hide  last-message">' + consulta + '<span class="message-time" style="margin-left:10px">' + getHoraActual() + '</span> </div><div class="clear"></div></div>';
        $('.chat-body').append(mensaje);
        $("#consultaChat").val("");

        setTimeout(function () {
            $('.last-spining').hide(400, function () {
                $('.last-message').fadeIn('fast');
                $('.last-spining').removeClass('last-spining');
                $('.last-message').removeClass('hide');
                $(".chat-body").scrollTop($(".chat-body")[0].scrollHeight);
            });
        }, 500);

        var text = '<div class="chat-bubble tu ojo-data"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid"><circle cx="0" cy="44.1678" r="15" fill="#ffffff"><animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate></circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff"> <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate></circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff"><animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate></circle></svg></div>';
        setTimeout(function () {
            $('.chat-body').append(text);
        }, 1000);


        $.ajax({
            url: "web/controller/controllerSQL.php",
            type: "POST",
            data: {message: consulta}

        }).done(function (result) {
            console.log(result);
            var respuesta = '<div class="chat-package"><div class="chat-bubble tu hide last-message">' + result + '<span class="message-time">' + getHoraActual() + '</span></div><div class="clear"></div></div>';
            $('.chat-body').append(respuesta);

            setTimeout(function () {
                $('.last-message').fadeIn('slow');
                $('.last-message').removeClass('hide');
                $(".chat-body").scrollTop($(".chat-body")[0].scrollHeight);
            }, 800);


        }).fail(function () {
            console.log("Error en ajax!!!");
        }).always(function () {
            console.log("Completado!!!!");
            $('.ojo-data').addClass('hide');
        });



    });

    //finalizar el chatbot
    $('.end-chat').click(function () {
        $('.chat-body').addClass('hide');
        $('.chat-input').addClass('hide');
        $('.chat-session-end').removeClass('hide');
        $('.chat-header-option').addClass('hide');
    });

});



function getHoraActual() {
    var date = new Date();
    var hora;
    var minutos;
    minutos = date.getMinutes();
    if (minutos < 10) {
        minutos = '0' + minutos;
    }
    hora = date.getHours() + ":" + minutos;
    return hora;
}


