$(function () {
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
})