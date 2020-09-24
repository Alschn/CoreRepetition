$(document).ready(function() {
    let display = false;
    $(".btn-comments").click(function () {
        if (display === false) {
            $(this).next(".comment-block").show("slow");
            display = true
        } else {
            $(this).next(".comment-block").hide("slow");
            display = false
        }
    })
});
