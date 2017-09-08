function closenotify(id) {
    $.post( "/notify/" + id );
    $( "#notify" + id ).remove();
}
function book_tag_add(id) {
    var formtagnew = "<form method=\"post\" action=\"/book/" + id + "/tagadd\">" +
    "<input class=\"form-control\" style=\"width: 100px; display: initial; \" name=\"tag\" type=\"text\">" +
    "<button class=\"btn btn-outline-success\"><i class=\"fa fa-floppy-o\"></i></button>" +
    "</form>";
    $(document).find( "#addtag" ).append( formtagnew );
}
function filter_tag_add(id) {
    var formtagnew = "<form method=\"post\" action=\"/filter/" + id + "/tagadd\">" +
    "<input class=\"form-control\" style=\"width: 100px; display: initial; \" name=\"tag\" type=\"text\">" +
    "<button class=\"btn btn-outline-success\"><i class=\"fa fa-floppy-o\"></i></button>" +
    "</form>";
    $(document).find( "#addtag" ).append( formtagnew );
}
function question_tag_add(id) {
    var formtagnew = "<form method=\"post\" action=\"/question/" + id + "/tagadd\">" +
    "<input class=\"form-control\" style=\"width: 100px; display: initial; \" name=\"tag\" type=\"text\">" +
    "<button class=\"btn btn-outline-success\"><i class=\"fa fa-floppy-o\"></i></button>" +
    "</form>";
    $(document).find( "#addtag" ).append( formtagnew );
}

function snippet_tag_add(id) {
    var formtagnew = "<form method=\"post\" action=\"/snippet/" + id + "/tagadd\">" +
    "<input class=\"form-control\" style=\"width: 100px; display: initial; \" name=\"tag\" type=\"text\">" +
    "<button class=\"btn btn-outline-success\"><i class=\"fa fa-floppy-o\"></i></button>" +
    "</form>";
    $(document).find( "#addtag" ).append( formtagnew );
}

function order_tag_add(id) {
    var formtagnew = "<form method=\"post\" action=\"/order/" + id + "/tagadd\">" +
    "<input class=\"form-control\" style=\"width: 100px; display: initial; \" name=\"tag\" type=\"text\">" +
    "<button class=\"btn btn-outline-success\"><i class=\"fa fa-floppy-o\"></i></button>" +
    "</form>";
    $(document).find( "#addtag" ).append( formtagnew );
}
function tag_add(id) {
    $.ajax({
        type: 'GET',
        url: '/tagdelete/' + id,

        success: function(msg) {
            $(document).find( "#tag" + id ).after( msg );
            $('#myModal').modal('show');
        }
    });
}
$(document).ready(function(){
    //Check to see if the window is top if not then display button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    // Прокрутка в начало
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0},800);
        return false;
    });
    // КОНЕЦ: Прокрутка в начало
});
