$(document).bind('pageinit',function(){

    $( ".on-off-switch" ).each(function(index) {
       var status = $(this).attr('data-devicestatus');
       var deviceId = $(this).attr('data-deviceid');
       console.log('Setting status of device: ' + deviceId + ':' + status);
       $(this).val(status.toLowerCase()).slider('refresh');

    });

    $( ".on-off-switch" ).bind( "change", function(event) {
      var deviceId = $(this).attr('data-deviceid');
      var status = $(this).attr('data-devicestatus');
      var newStatus = status == 'ON' ? 'OFF':'ON';

      var url = '/device/'+deviceId+'/'+newStatus;

      $.post(url,function(data){
        // var device = JSON.parse(data);
        console.log('Got back: ' + data);
        // var newStatus = device.status;
        // console.log($('#device'+device.deviceId));
        // console.log('Status after: ' + $('#device'+device.deviceId).attr('data-devicestatus'));
        // $('#device'+device.deviceId).attr('data-devicestatus', newStatus);
        // console.log('Status after: ' + $('#device'+device.deviceId).attr('data-devicestatus'));
        //$('#device'+device.deviceId).val(newStatus.toLowerCase()).slider('refresh');

      });
      $(this).attr('data-devicestatus', newStatus);
      console.log('Status after: ' + $(this).attr('data-devicestatus'));
    });
});

