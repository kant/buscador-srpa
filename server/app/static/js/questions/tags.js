$(function () {
    var tagsTemplate = function (tagList, questionId, tagType) {
        var content = '';
        for (var i = 0; i < tagList.length; i++) {
            var button = '<button class="btn btn-primary" data-question-id="qid" data-tag-type="tagtype" data-sort="dsort">text</button>';
            button = button.replace('text', tagList[i])
                .replace('qid', questionId)
                .replace('tagtype', tagType)
                .replace('dsort', i.toString());
            content += button;
        }
        content = '<div class="tag-list">' + content + '</div>';
        var cancelButton = '<button class="btn btn-default" data-question-id="' + questionId + '">Cancelar</button>';
        var addButton = '<button class="btn btn-success disabled">Agregar tag</button>';
        content += '<div class="menu">' + cancelButton + addButton + '</div>';
        var searchField = '<input type="text" placeholder="Busqueda rápida" class="suggest-search">' ;
        var orderSelect = '<label>Ordenar según <select id="tag-order"><option value="suggestion">relevancia</option><option value="alphabetically">nombre</option></select></label>';
        content += '<div class="search-and-order">' + orderSelect + searchField + '</div>';
        content = '<div class="tag-suggester">' + content + '</div>';
        var $content = $(content);
        $content.find('#tag-order').data('tags', tagList);
        return $content;
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
    };

    var selectTag = function (e) {
        $(e.currentTarget).addClass('active')
            .siblings().removeClass('active')
            .parents('.qtip-jgm').find('.btn-success').removeClass('disabled');

    };

    var showTags = function (api, questionId, tagType) {
        var url;
        if (tagType == 'topic') {
            url = '/pregunta/' + questionId + '/sugerir_ministerio';
        } else {
            url = '/pregunta/' + questionId + '/sugerir_area';
        }
        $.ajax({
            url: url,
            method: 'GET'
        }).then(function (response) {
            var content = tagsTemplate(response, questionId, tagType);
            api.set('content.text', content);
            initializeLunr(response, content);
        });
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
    };

    var changeOrder = function (e) {
        var $select = $(e.currentTarget);
        var tags = $select.data('tags');
        var order = $select.val();
        var buttons = $select.parents('.tag-suggester').find('.tag-list button');
        if (order == 'alphabetically') {
            buttons.sort(function (a, b) {
                return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
            });
        } else {
            buttons.sort(function (a, b) {
                var originalPositionA = parseInt($(a).data('sort'));
                var originalPositionB = parseInt($(b).data('sort'));
                return (originalPositionA < originalPositionB) ? -1 : 1;

            });
        }
        $select.parents('.tag-suggester').find('.tag-list').html(buttons);
    };

    var initializeLunr = function (tagList, suggesterEl) {
        var searcher = lunr(function () {
            this.field('name');
            this.ref('id');
        });
        for (var i=0; i<tagList.length; i++) {
            var tag = {
                name: tagList[i],
                id: i
            };
            searcher.add(tag);
        }
        suggesterEl.find('.suggest-search').data('searcher', searcher);
    };

    var filterResults = function (e) {
        var $select = $(e.currentTarget);
        var query = $select.val().trim();
        var tagList = $select.parents('.tag-suggester').find('.tag-list');
        if (query.length > 0) {
            var searcher = $select.data('searcher');
            var results = searcher.search(query);
            tagList.find('button').addClass('hidden');
            for (var i=0; i<results.length; i++) {
                var tagId = results[i].ref;
                tagList.find('button[data-sort="' + tagId.toString() + '"]').removeClass('hidden');
            }
        } else {
            tagList.find('button').removeClass('hidden');
        }
    };

    var $body = $('body');
    $body.on('click', '.qtip-jgm button.btn-primary', selectTag);
    $body.on('click', '.qtip-jgm button.btn-success', submitTags);
    $body.on('click', '.result .btn.without-topic', function (e) {
        loadTags(e, 'topic');
    });
    $body.on('click', '.result .btn.without-subtopic', function (e) {
        loadTags(e, 'subtopic');
    });
    $body.on('click', '.qtip-jgm button.btn-default', function (e) {
        var $button = $(e.currentTarget);
        var questionId = $button.data('question-id');
        var tooltip = $button.parents('.qtip-jgm');
        var tagType = tooltip.find('.btn-primary').data('tag-type');
        $('.result[data-question-id=' + questionId + '] .without-' + tagType).removeClass('disabled');
        tooltip.remove();
    });
    $body.on('change', '.qtip-jgm #tag-order', changeOrder);
    $body.on('change keyup', '.qtip-jgm .suggest-search', filterResults)
});
