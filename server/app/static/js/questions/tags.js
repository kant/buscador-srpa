$(function () {
    var tagsTemplate = function (tagList, questionId, tagType) {
        var content = '';
        for (var i = 0; i < tagList.length; i++) {
            var button = '<button class="btn btn-primary" data-question-id="qid" data-tag-type="tagtype">text</button>';
            button = button.replace('text', tagList[i]);
            button = button.replace('qid', questionId);
            button = button.replace('tagtype', tagType);
            content += button;
        }
        content = '<div class="tag-list">' + content + '</div>'
        var cancelButton = '<button class="btn btn-default" data-question-id="' + questionId + '">Cancelar</button>';
        var addButton = '<button class="btn btn-success disabled">Agregar tag</button>';
        content += '<div class="menu">' + cancelButton + addButton + '</div>'
        content = '<div class="tag-suggester">' + content + '</div>'
        return $(content);
    };

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

    var selectTag = function (e) {
        $(e.currentTarget).addClass('active')
            .siblings().removeClass('active')
            .parents('.qtip-jgm').find('.btn-success').removeClass('disabled');

    };

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
            var content = tagsTemplate(response, questionId, tagType);
            api.set('content.text', content);
        })
        return ''
    };

    var submitTags = function (e) {
        var $submitButton = $(e.currentTarget).text('Procesando...').addClass('disabled');
        var $tagButton = $submitButton.parents('.qtip-jgm').find('.btn-primary.active');
        var questionId = $tagButton.data('question-id');
        var tagText = $tagButton.text();
        var tagType = $tagButton.data('tag-type');
        var data = {};
        data[tagType] = tagText;
        $.ajax({
            url: '/pregunta/id/actualizar'.replace('id', questionId),
            method: 'POST',
            data: data
        }).then(function (response) {
            $tagButton.parents('.qtip-jgm').remove();
            $('.result[data-question-id=' + questionId + ']').replaceWith($(response));
            if (window.jgm.best_words) {
                window.jgm.results.highlight(questionId, window.jgm.best_words[questionId]);
            }
        })
    }

    $('body').on('click', '.qtip-jgm button.btn-primary', selectTag);
    $('body').on('click', '.qtip-jgm button.btn-success', submitTags);
    $('body').on('click', '.result .btn.without-topic', function (e) {
        loadTags(e, 'topic');
    });
    $('body').on('click', '.result .btn.without-subtopic', function (e) {
        loadTags(e, 'subtopic');
    });
    $('body').on('click', '.qtip-jgm button.btn-default', function (e) {
        var $button = $(e.currentTarget);
        var questionId = $button.data('question-id');
        var tooltip = $button.parents('.qtip-jgm');
        var tagType = tooltip.find('.btn-primary').data('tag-type')
        $('.result[data-question-id=' + questionId + '] .without-' + tagType).removeClass('disabled');
        tooltip.remove();
    });
})