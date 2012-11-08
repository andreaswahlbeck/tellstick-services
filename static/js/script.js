$(document).ready(function(){

    console.log('getting units from telldus')

    $.get('/status', function(data) {

        console.log('Got data: ' + data);

        devices = JSON.parse(data);

        $.each(devices, function(i){
            console.log(devices[i]);
            var deviceDiv = $('<div />');
            $(deviceDiv).append('<h2>' + devices[i].deviceId + '-' + devices[i].deviceName + '</h2>');
            $(deviceDiv).append('<p>Status: ' + devices[i].status + '</p>');
            $('#content-wrapper').append(deviceDiv);

        });

    });


});
