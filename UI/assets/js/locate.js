
function getLocation(){
    var msg; 
    if('geolocation' in navigator){
      requestLocation();
    }else{
      msg = "no geolocation";
      outputResult(msg);
      $('.buttonclick').removeClass('buttonclick').addClass('buttonclick-success'); 
    }
  
function requestLocation(){

  var options = {
    enableHighAccuracy: false,
    timeout: 5000,
    maximumAge: 0
  };

  navigator.geolocation.getCurrentPosition(success, error, options); 

  function success(pos){
    var lng = pos.coords.longitude;
    var lat = pos.coords.latitude;
    msg = 'Incidence happened at longitude: ' + lng + ' and latitude: ' + lat ;
    outputResult(msg); 
    $('.buttonclick').removeClass('buttonclick').addClass('buttonclick-success'); 
  }

  function error(err){
    msg = 'Error: ' + err + ' :(';
    outputResult(msg); 
    $('.buttonclick').removeClass('buttonclick').addClass('buttonclick-error'); 
   }  
}

function outputResult(msg){
  $('.result').addClass('result').html(msg);
}
} 

// attach getLocation() to button click
$('.buttonclick').on('click', function(){
    $('.result').html('<i class="fa fa-spinner fa-spin"></i>');
  getLocation();
});
