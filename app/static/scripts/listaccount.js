$(document).ready(function() {

    $(".place").click(function() {
        $.ajax({
            url: '/ctryrmv',
            type: 'POST',
            data: JSON.stringify({  response: $(this).attr('id'),
                                    list:  $(this).parent().attr('id') }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                $("#"+response['col']).children("#"+response['response']).remove();
            }
        });
    });

    $(".place").hover(function() {
        $(this).children("i").removeClass("d-none");
    },function() {
        $(this).children("i").addClass("d-none");
    });
});