$(function () {
    $('.main').on('click', '.result .edit', function (e) {
        var question = $(e.currentTarget).closest('.result');
        var questionId = question.data('question-id');
        var modal = $('#question-editor').modal({'show': true});
        modal.find('.modal-body').html('');

        var url = '/pregunta/' + questionId.toString() + '/editar';
        var options = {standalone: true};
        var callback = function (response) {
            response = $(response);
            response.attr('action', url);
            modal.find('.modal-body').html(response);
        };
        $.get(url, options, callback);
    });
});