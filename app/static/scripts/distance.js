//  Calculate the distance between two points in latitude and longitude
$(document).ready(function() {
    navigator.geolocation.getCurrentPosition(showPosition);
});

function showPosition(position){
    var lat = position.coords.latitude;
    var long = position.coords.longitude;

    $.ajax({
        // Specify the endpoint URL the request should be sent to.
        url: '/coords',
        // The request type.
        type: 'POST',
        // The data, which is now most commonly formatted using JSON because of its
        // simplicity and is native to JavaScript.
        data: JSON.stringify({ response: $('#countryName').text() }),
        // Specify the format of the data which will be sent.
        contentType: "application/json; charset=utf-8",
        // The data type itself.
        dataType: "json",
        // Define the function which will be triggered if the request is received and 
        // a response successfully returned.
        success: function(response){
            // console.log(distanceInKm(lat,long,response['lat'],response['lang']));
            kms = distanceInKm(lat,long,response['lat'],response['lang']);
            kms = kms.toFixed(2);
            
            // insert the distance in the html after #capital
            $('#capital').after('<div class="row justify-content-center"><h4 class="text-center" id="distance">(You are ' + kms + 'km away from '+ response['city']+')</h4></div>');
        },
        // The function which will be triggered if any error occurs.
        error: function(error){
            console.log(error);
        }
    });
}

function distanceInKm(lat,long,lat2,long2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat);  // deg2rad below
    var dLon = deg2rad(long2-long); 
    var a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat)) * Math.cos(deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2); 

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    var d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI/180)
}