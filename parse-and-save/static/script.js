$(document).ready(function () {

    $('.progress').fadeOut();


    $('#check-updates').click(function () {

        console.log('Clicked')


        
        var socket = io.connect('http://127.0.0.1:5000/');


        socket.emit('update');

        socket.on('update_response', function(data){
            
            if(data.articles && Number(data.articles) !== 0){
                $('.progress-text-response').text(
                    '<p>There are '+data.articles+' new articles.<br> Parsing...</p>'
                );
            }
        })


        socket.on('recieve_articles', function(data){
            $('.progress').fadeIn();
        })

    
    })

})
