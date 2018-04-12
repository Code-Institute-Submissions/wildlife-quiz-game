$(function() {
    $('button').click(function() {
        var guess = $('#guess').val();
        $.ajax({
            url: '/game',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});