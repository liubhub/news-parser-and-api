$(document).ready(function () {

    $('.progress').fadeOut();


    $('#check-updates').click(function () {

        console.log('Clicked')


        $('.progress').fadeIn();
        
        var socket = io.connect('http://127.0.0.1:5000/');


        socket.emit('update');

        socket.on('update_response', function(data){
            console.log(data)
        })
        // var source = new EventSource("/update");

        // source.onmessage = function (event) {

        //     console.log(event.data)

        //     $('.progress-bar').css('width', event.data + '%').attr('aria-valuenow', event.data);
        //     $('.progress-bar-label').text(event.data + '%');

        //     if (event.data == 100) {
        //         source.close()
        //     }
        // }

    })



})
