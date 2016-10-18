window.jgm = window.jgm || {};
window.jgm.results = {
    highlight: function (questionId, words) {
        // TODO: tener en cuenta que words son las palabras procesadas (sin tildes, en minusculas)
        var questionText = $('.result[data-question-id=' + questionId + '] p.question-body');
        for (var i = 0; i < words.length; i++) {
            questionText.highlight(words[i]);
        }
    },
    bindEvents: function () {
        $('.result .delete').on('click', function (e) {
            $(e.currentTarget).closest('.result').addClass('confirm-delete')
        });
        $('.result .cancel-delete').on('click', function (e) {
            $(e.currentTarget).closest('.result').removeClass('confirm-delete')
        });
        $('.result .confirm-delete').on('click', function (e) {
            var questionId = $(e.currentTarget).closest('.result').data('question-id');
            var url = '/pregunta/' + questionId + '/borrar';
            var callback = function (response) {
                if (response && response.success) {
                    location.reload();
                }
            };
            $.post(url, {}, callback);
        })
    }
};

$(function () {
    window.jgm.results.bindEvents();
});