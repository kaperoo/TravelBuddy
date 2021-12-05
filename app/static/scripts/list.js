$(document).ready(function() {

    $(".crow").hover(function() {
        var classname = $(this).attr('id');

        $("svg path[name=\"" + classname + "\"]").css({
            fill: "#dfbd69",
            transition: "0.6s"
        });
    });
    $(".crow").mouseleave(function() {
        var classname = $(this).attr('id');

        $("svg path[name=\"" + classname + "\"]").css("fill", "#0a2d3b");
    });
    $(".crow").click(function() {
        var classname = $(this).attr('id');

        window.location = "/country/" + classname;
    });
});