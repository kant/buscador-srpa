window.jgm = window.jgm || {};
window.jgm.results = {
    highlight: function (questionId, words) {
        // TODO: tener en cuenta que words son las palabras procesadas (sin tildes, en minusculas)
        var questionText = $('.result[data-question-id=' + questionId + '] p.question-body');
        for (var i = 0; i < words.length; i++) {
            questionText.highlight(words[i]);
        }
    },
    bindDeleteEvents: function () {
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
    },
    bindTagEvents: function () {
        $('button').tooltip({html:true, trigger: 'manual', placement: 'right'});

        $('.result .btn.without-topic').on('click', function(e) {
        });
        $('.result .btn.without-subtopic').on('click', function(e) {
            var $button = $(e.currentTarget);
            var questionId = $button.closest('.result').data('question-id');
            $button.tooltip('show').addClass('disabled');
            $.post('/pregunta/' + questionId + '/sugerir_subtema', {}, function (response) {
                var html = ''
                for (var i=0; i<response.length; i++) {
                    html += '<button type="button" class="btn btn-subtopic">' + response[i] + '</button>'
                }
                $button.siblings('.tooltip').find('.tooltip-inner').html(html);
            })
        });
    },
    bindEvents: function () {
        this.bindTagEvents();
        this.bindDeleteEvents();
    }
};

$(function () {
    window.jgm.results.bindEvents();
});