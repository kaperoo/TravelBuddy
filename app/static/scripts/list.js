$(document).ready(function() {

    $(".user").click(function() {
        var username = $(this).attr('id');
        window.location = "/profile/" + username;
    });
    $(".place").click(function() {
        var country = $(this).attr('id');
        window.location = "/country/" + country;
    });

    $("#l1").hover(function() {
        $(".iliv").addClass("fa-times");
        $(".iliv").removeClass("fa-check");
    },function() {
        $(".iliv").removeClass("fa-times");
        $(".iliv").addClass("fa-check");
    });
    $("#b1").hover(function() {
        $(".ibuc").addClass("fa-times");
        $(".ibuc").removeClass("fa-check");
    },function() {
        $(".ibuc").removeClass("fa-times");
        $(".ibuc").addClass("fa-check");
    });
    $("#v1").hover(function() {
        $(".ivis").addClass("fa-times");
        $(".ivis").removeClass("fa-check");
    },function() {
        $(".ivis").removeClass("fa-times");
        $(".ivis").addClass("fa-check");
    });
    
    $(".dbb").click(function() {
        $.ajax({
            url: '/respond',
            type: 'POST',
            data: JSON.stringify({ response: $(this).attr('id'),
                                    country: $("#countryName").text() }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);
            }
        });
    });
});