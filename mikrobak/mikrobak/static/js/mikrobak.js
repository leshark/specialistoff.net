function get_backup(id) {
    var sendData = "";
    $.ajax({
        type: "POST",
        dataType: "json",
        contentType:"application/json; charset=utf-8",
        url: "/device/" + id + "/backupdl",
        data: sendData,
        success: function(result) {
            $("#backuptext").text(result.settings);
        },
        error: function(msg) {
            console.log("%s %s" ,xhr,type);
            return false;
        }
    });
    return false;
};
$(document).ready(function(){
    //Check to see if the window is top if not then display button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    //Click event to scroll to top
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0},800);
        return false;
    });

});
