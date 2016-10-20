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
            })
        }

        $('body').on('click', '.qtip-jgm button', submitTags);

        $('.result .btn.without-topic').on('click', function (e) {
            loadTags(e, 'topic');
        });
        $('.result .btn.without-subtopic').on('click', function (e) {
            loadTags(e, 'subtopic');
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