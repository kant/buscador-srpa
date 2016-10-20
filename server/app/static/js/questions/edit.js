$(function () {
    $('.main').on('click', '.result .edit', function (e) {
        var question = $(e.currentTarget).closest('.result');
        var questionId = question.data('quesiton-id');
        $('#question-editor').modal({'show': true})
    });
})