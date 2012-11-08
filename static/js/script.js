$(document).ready(function(){

    console.log('getting units from telldus')

    // $.get('/status', function(data) {

    //     console.log('Got data: ' + data);

    //     devices = JSON.parse(data);

    //     $.each(devices, function(i){
    //         console.log(devices[i]);
    //         var deviceDiv = $('<div />');
    //         $(deviceDiv).append('<h2>' + devices[i].deviceId + '-' + devices[i].deviceName + '</h2>');
    //         $(deviceDiv).append('<p>Status: ' + devices[i].status + '</p>');
    //         $('#content-wrapper').append(deviceDiv);

    //     });

    // });


    $('.basic').toggle({
      onClick: function (event, status) {}, // Do something on status change if you want
      text: {
        enabled: false, // Change the enabled disabled text on the fly ie: 'ENABLED'
        disabled: false // and for 'DISABLED'
      },
      style: {
        enabled: 'primary', // default button styles like btn-primary, btn-info, btn-warning just remove the btn- part.
        disabled: false // same goes for this, primary, info, warning, danger, success. 
      }
    });

});
