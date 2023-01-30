
var fechaHora = function () {
    let currentDate = new Date(),
            hours = currentDate.getHours(),
            minutes = currentDate.getMinutes(),
            seconds = currentDate.getSeconds(),
            weekDay = currentDate.getDay(),
            day = currentDate.getDate(),
            month = currentDate.getMonth(),
            year = currentDate.getFullYear();

    const dias = [
        'Domingo',
        'Lunes',
        'Martes',
        'Miercoles',
        'Jueves',
        'Viernes',
        'Sábado'
    ];

    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    if (day < 10) {
        day = '0' + day;
    }

    document.getElementById('hours').textContent = dias[weekDay] + " " + day + ", " + hours + ":" + minutes;
};
fechaHora();