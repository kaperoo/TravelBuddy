$(document).ready(function() {

    // highlight the map when hovering over a list
    $(".crow").hover(function() {
        var classname = $(this).attr('id');

        $("svg path[name=\"" + classname + "\"]").css({
            fill: "#dfbd69",
            transition: "0.6s"
        },);
    });
    $(".crow").mouseleave(function() {
        var classname = $(this).attr('id');

        $("svg path[name=\"" + classname + "\"]").css("fill", "#0a2d3b");
    });

    // go to the clicked country page
    $(".crow").click(function() {
        var classname = $(this).attr('id');

        window.location = "/country/" + classname;
    });

    // highlight the list when hovering over a map
    $("svg path").hover(function() {
        var name = $(this).attr('name');

        // name = name.split(" ");
        row = document.getElementById(name);
        row.scrollIntoView();

        $(".crow[id=\""+name+"\"]").css({
            "background-color": "#dfbd69",
            transition: "0.6s",
            "font-weight": "bold"
        });
    });
    $("svg path").mouseleave(function() {
        var name = $(this).attr('name');

        $(".crow[id=\""+name+"\"]").css({
            "background-color": "#0a525f",
            "font-weight": "normal",
        });
    });

    // go to the clicked country page
    $("svg path").click(function() {
        var name = $(this).attr('name');

        window.location = "/country/" + name;
    });

    // scale the scroll area appropriately to the position and window size
    $(window).resize(function() {
        var scrollP = $(".scrollable").position();
        $(".scrollable").css({
            height: "calc(100vh - 40px - "+ scrollP.top + "px)"
        });
    });
    $(document).ready(function() {
        var scrollP = $(".scrollable").position();
        $(".scrollable").css({
            height: "calc(100vh - 40px - "+ scrollP.top + "px)"
        });
    });
});