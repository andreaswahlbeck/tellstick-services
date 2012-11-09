$(document).bind('pageinit',function(){
    var closeInterval;

    var showFailed = function() {
        console.log("Displaying message: ");
        $("#failed-popup").popup("open");
    };

    $( "#failed-popup" ).bind({
       popupafteropen: function(event, ui) {
          closeInterval = self.setInterval(function(){
            $("#failed-popup").popup('close');
          }, 2000);

       },
       popupafterclose: function(event, ui) {
          window.clearInterval(closeInterval);
       }
    });

    $( ".on-off-switch" ).each(function(index) {
       var status = $(this).attr('data-devicestatus');
       var deviceId = $(this).attr('data-deviceid');
       console.log('Setting status of device: ' + deviceId + ':' + status);
       $(this).val(status.toLowerCase()).slider('refresh');

    });

    $(".on-off-switch" ).bind( "change", function(event) {
      var deviceId = $(this).attr('data-deviceid');
      var status = $(this).attr('data-devicestatus');
      var newStatus = status == 'ON' ? 'OFF':'ON';

      var url = '/device/'+deviceId+'/'+newStatus;

      $.post(url,function(data,deviceId,status){
        console.log('Got back: ' + data);

        var device = JSON.parse(data);

        if (device.error) {
          console.log('got error back...');
          var oldStatus = $('#device'+device.deviceId).attr('data-devicestatus');

          console.log('resoring status: ' + oldStatus);
          $('#device'+device.deviceId).val(oldStatus.toLowerCase()).slider('refresh');
          showFailed();
        } else {
          $('#device'+device.deviceId).attr('data-devicestatus', device.status);
        }

      });

    });

    $("#refresh-button").bind('click', function() {
        $.get('/status',function(data) {
            var devices = JSON.parse(data);
            $(devices).each(function(index){
              var status = devices[index].status;
              var deviceId = devices[index].deviceId;

              $('#device'+deviceId).attr('data-devicestatus', status).val(status.toLowerCase()).slider('refresh');
            });
        });
    });

});

