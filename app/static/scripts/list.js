$(document).ready(function() {

    $(".user").click(function() {
        var username = $(this).attr('id');
        window.location = "/profile/" + username;
    });
    $(".place").click(function() {
        var country = $(this).attr('id');
        window.location = "/country/" + country;
    });

    // $(".visited").hover(function() {
    //     $(this).css({"margin-top": "10px",
    //         "border-style": "solid",
    //         "border-radius": "5px",
    //         "border-color": "#72c376",
    //         "background-color": "transparent",
    //         "color": "white",});
    // });
});