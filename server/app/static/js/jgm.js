window.jgm = window.jgm || {};
window.jgm.results = {
    highlight: function (questionId, words) {
        // TODO: tener en cuenta que words son las palabras procesadas (sin tildes, en minusculas)
        var questionText = $('.result[data-question-id=' + questionId + '] p.question-body');
        questionText.highlight(words);
    },
    bindDeleteEvents: function () {
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
    },
    bindEditEvents: function () {
        $('.main').on('click', '.result .edit', function (e) {
            var question = $(e.currentTarget).closest('.result');
            var questionId = question.data('quesiton-id');
            $('#question-editor').modal({'show': true})
        });
    },
    bindEvents: function () {
        this.bindDeleteEvents();
        this.bindEditEvents();
    }
};

$(function () {
    window.jgm.results.bindEvents();
});