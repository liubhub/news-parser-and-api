$(document).ready(function () {

    $('.progress').fadeOut();


    $('#check-updates').click(function () {

        console.log('Clicked')
        $('.progress').fadeIn();
        

        var source = new EventSource("/update");

        source.onmessage = function (event) {

            console.log(event.data)

            $('.progress-bar').css('width', event.data + '%').attr('aria-valuenow', event.data);
            $('.progress-bar-label').text(event.data + '%');

            if (event.data == 100) {
                source.close()
            }
        }

    })



})
