window.jgm = window.jgm || {};
window.jgm.results = {
    highlight: function (questionId, words) {
        // TODO: tener en cuenta que words son las palabras procesadas (sin tildes, en minusculas)
        var questionText = $('.result[data-question-id=' + questionId + '] p.question-body');
        questionText.highlight(words);
    }
};

$(function () {
    $(document).ajaxStart(NProgress.start);
    $(document).ajaxStop(NProgress.done);
    $(window).on('beforeunload', function() {
        NProgress.start();
        return undefined;
    })
})

