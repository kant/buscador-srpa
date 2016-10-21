$(function () {
    $('.main').on('click', '.result .delete', function (e) {
        $(e.currentTarget).closest('.result').addClass('confirm-delete')
    });
    $('.main').on('click', '.result .cancel-delete', function (e) {
        $(e.currentTarget).closest('.result').removeClass('confirm-delete')
    });
    $('.main').on('click', '.result .confirm-delete', function (e) {
        var questionId = $(e.currentTarget).closest('.result').data('question-id');
        var url = '/pregunta/' + questionId + '/borrar';
        var callback = function (response) {
            if (response && response.success) {
                if (window.location.pathname.substr(0, 9) == '/pregunta') {
                    window.location.pathname = '/buscar'
                } else {
                    location.reload();
                }
            }
        };
        $.post(url, {}, callback);
    })
})