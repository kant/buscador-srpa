$(function() {
    $('#search-filters .add-filter').on('click', function() {
        $('#search-filters .add-filter-container').addClass('hidden');
        $('#filter-picker').removeClass('hidden');
    });
    $('#search-filters .cancel-filter').on('click', function() {
        $('#search-filters .add-filter-container').removeClass('hidden');
        $('#filter-picker').addClass('hidden');
    });
    var showValuePicker = function() {
        var behaviourSelected = $('#search-filters #filter-behaviour option:selected').val()
        var optionSelected = $('#search-filters #filter-type option:selected').val();
        $('#search-filters .filter-value').addClass('hidden').removeClass('active');

        if (behaviourSelected == 'has-value') {
            $('#search-filters .filter-value[data-filter-type="' + optionSelected + '"]').removeClass('hidden').addClass('active');
            $('#search-filters #filter-comparision-container').removeClass('hidden');
        } else if (behaviourSelected == 'without-value') {
            $('#search-filters #filter-comparision-container').addClass('hidden');
            $('#search-filters .filter-value').addClass('hidden');
        }
    };

    var urlConstructor = function (args) {
        var getArgs = [];
        for (var key in args) {
            getArgs.push(encodeURIComponent(key) + '=' + encodeURIComponent(args[key]));
        }
        return '/buscar?' + getArgs.join('&');
    };

    var currentArgs = function () {
        var args = jQuery.extend({}, window.jgm.query.filters);
        if (window.jgm.query.text) {
            args['q'] = window.jgm.query.text;
        }
        return args;
    };

    var updateRemoveLinks = function () {
        var links = $('a.filter-link[data-filter-link-type="remove"]');
        for (var i=0; i<links.length; i++) {
            var link = $(links[i]);
            var newArgs = currentArgs();
            delete newArgs[link.data('filter-name')];
            var newHref = urlConstructor(newArgs);
            link.attr('href', newHref);
        }
    };

    var updateAddLink = function () {
        var selectedFilterName = $('#search-filters #filter-type option:selected').val();
        var selectedFilterValue = $('#search-filters .filter-value.active option:selected').val();
        var link= $('#search-filters #apply-filter');
        var newArgs = currentArgs();
        var translations = {
            'informe': 'informe', 'autor': 'autor',
            'ministerio': 'tema', 'área de gestión': 'subtema'
        };
        newArgs[translations[selectedFilterName]] = selectedFilterValue;
        var newHref = urlConstructor(newArgs);
        link.attr('href', newHref);
    };

    $('#search-filters #filter-behaviour').select2({
        minimumResultsForSearch: Infinity
    })
    $('#search-filters #filter-comparision').select2({
        minimumResultsForSearch: Infinity
    })
    $('#search-filters #filter-type').select2({
        minimumResultsForSearch: Infinity
    })
    $('#search-filters .filter-value-picker').select2()
    $('#search-filters').on('select2:select', function () {
        showValuePicker();
        updateAddLink();
    })

    showValuePicker();
    updateRemoveLinks();
    updateAddLink();
})