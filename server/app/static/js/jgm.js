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
    bindTagEvents: function () {
        var loadTags = function (e, tagType) {
            var $button = $(e.currentTarget).addClass('disabled');
            var questionId = $button.closest('.result').data('question-id');
            $button.qtip({
                content: {
                    text: function (event, api) {
                        return showTags(api, questionId, tagType)
                    }
                },
                position: {
                    my: 'center left',
                    at: 'center right'
                },
                hide: false,
                style: {
                    classes: 'qtip-jgm'
                }
            }).qtip('show')
        }

        var showTags = function (api, questionId, tagType) {
            var url;
            if (tagType == 'topic') {
                url = '/pregunta/' + questionId + '/sugerir_tema';
            } else {
                url = '/pregunta/' + questionId + '/sugerir_subtema';
            }
            $.ajax({
                url: url,
                method: 'GET'
            }).then(function (response) {
                content = '';
                for (var i = 0; i < response.length; i++) {
                    var button = '<button class="btn btn-primary" data-question-id="qid" data-tag-type="tagtype">text</button>';
                    button = button.replace('text', response[i]);
                    button = button.replace('qid', questionId);
                    button = button.replace('tagtype', tagType);
                    content += button;
                }
                api.set('content.text', $(content));
            })
            return 'Cargando...'
        };

        var submitTags = function (e) {
            var $button = $(e.currentTarget);
            var questionId = $button.data('question-id');
            var tagText = $button.text();
            var tagType = $button.data('tag-type');
            var data = {};
            data[tagType] = tagText;
            $.ajax({
                url: '/pregunta/id/actualizar'.replace('id', questionId),
                method: 'POST',
                data: data
            }).then(function (response) {
                $button.parents('.qtip-jgm').remove();
                $('.result[data-question-id=' + questionId + ']').replaceWith($(response));
                window.jgm.results.highlight(questionId, window.jgm.best_words[questionId]);
            })
        }

        $('body').on('click', '.qtip-jgm button', submitTags);
        $('body').on('click', '.result .btn.without-topic', function (e) {
            loadTags(e, 'topic');
        });
        $('body').on('click', '.result .btn.without-subtopic', function (e) {
            loadTags(e, 'subtopic');
        });
    },
    bindEditEvents: function () {
        $('.main').on('click', '.result .edit', function (e) {
            var question = $(e.currentTarget).closest('.result');
            var questionId = question.data('quesiton-id');
            $('#question-editor').modal({'show': true})
        });
    },
    bindEvents: function () {
        this.bindTagEvents();
        this.bindDeleteEvents();
        this.bindEditEvents();
    }
};

$(function () {
    window.jgm.results.bindEvents();
});