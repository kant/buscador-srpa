$(function () {
    function deleteQuestion(e) {
        $(e.currentTarget).closest('.result').addClass('confirm-delete')
    }

    function cancelDelete(e) {
        $(e.currentTarget).closest('.result').removeClass('confirm-delete')
    }

    function confirmDelete(e) {
        var questionId = $(e.currentTarget).closest('.result').data('question-id');
        var url = '/pregunta/' + questionId + '/borrar';
        var callback = function (response) {
            if (response && response.success) {
                location.reload();
            }
        };
        $.post(url, {}, callback);
    }

    $('.main').on('click', '.result .delete', deleteQuestion)
        .on('click', '.result .cancel-delete', cancelDelete)
        .on('click', '.result .confirm-delete', confirmDelete)
});