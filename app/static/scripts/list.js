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
                
                if (response['response']=='v1'){
                    $("#v1").attr("id","v2");
                    $("#v2 h4").text("Mark as Visited");
                    $(".ivis").addClass("d-none");
                    $("#vs #"+response['username']).remove();
                }
                else if (response['response']=='v2'){
                    $("#v2").attr("id","v1");
                    $("#v1 h4").text("Visited");
                    $(".ivis").removeClass("d-none");
                    $("#vs").append("<div class='row vis pl-2 pt-1 rgreen' id='"+response['username']+"'><h4>@"+response['username']+"</h4></div>");
                }
                else if (response['response']=='b1'){
                    $("#b1").attr("id","b2");
                    $("#b2 h4").text("Add to Bucket List");
                    $(".ibuc").addClass("d-none");
                    $("#bs #"+response['username']).remove();
                }
                else if (response['response']=='b2'){
                    $("#b2").attr("id","b1");
                    $("#b1 h4").text("On Bucket List");
                    $(".ibuc").removeClass("d-none");
                    $("#bs").append("<div class='row fvis pl-2 pt-1 ryellow' id='"+response['username']+"'><h4>@"+response['username']+"</h4></div>");
                }
                else if (response['response']=='l1'){
                    $("#l1").attr("id","l2");
                    $("#l2 h4").text("Mark as Home");
                    $(".iliv").addClass("d-none");
                    $("#ls #"+response['username']).remove();
                }
                else if (response['response']=='l2'){
                    $("#l2").attr("id","l1");
                    $("#l1 h4").text("You Live Here");
                    $(".iliv").removeClass("d-none");
                    $("#ls").append("<div class='row liv pl-2 pt-1 rpurple' id='"+response['username']+"'><h4>@"+response['username']+"</h4></div>");
                }
            }
        });
    });
});