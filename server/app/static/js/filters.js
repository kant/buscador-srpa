$(function() {
    var searchFilters = $('#search-filters');

    searchFilters.find('.add-filter').on('click', function() {
        searchFilters.find('.add-filter-container').addClass('hidden');
        $('#filter-picker').removeClass('hidden');
    });
    searchFilters.find('.cancel-filter').on('click', function() {
        searchFilters.find('.add-filter-container').removeClass('hidden');
        $('#filter-picker').addClass('hidden');
    });
    var showValuePicker = function() {
        var behaviourSelected = searchFilters.find('#filter-behaviour option:selected').val();
        var optionSelected = searchFilters.find('#filter-type option:selected').val();
        searchFilters.find('.filter-value').addClass('hidden').removeClass('active');

        if (behaviourSelected == 'has-value') {
            searchFilters.find('.filter-value[data-filter-type="' + optionSelected + '"]').removeClass('hidden').addClass('active');
            searchFilters.find('#filter-comparision-container').removeClass('hidden');
        } else if (behaviourSelected == 'without-value') {
            searchFilters.find('#filter-comparision-container').addClass('hidden');
            searchFilters.find('.filter-value').addClass('hidden');
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
            delete newArgs[link.data('filter-name') + '-comparacion'];
            var newHref = urlConstructor(newArgs);
            link.attr('href', newHref);
        }
    };

    var updateAddLink = function () {
        var selectedBehaviour = searchFilters.find('#filter-behaviour option:selected').val();
        var selectedFilterName = searchFilters.find('#filter-type option:selected').val();
        var newArgs = currentArgs();
        var translations = {
            'informe': 'informe', 'autor': 'autor',
            'ministerio': 'ministerio', 'área de gestión': 'area'
        };

        if (selectedBehaviour == 'has-value') {
            newArgs[translations[selectedFilterName]] = searchFilters.find('.filter-value.active option:selected').val();

            var selectedComparision = searchFilters.find('#filter-comparision option:selected').val();
            var comparisionTranslation = {
                'different-to': 'diferencia',
                'equal-to': 'igualdad'
            };
            newArgs[translations[selectedFilterName] + '-comparacion'] = comparisionTranslation[selectedComparision];
        } else {
            newArgs[translations[selectedFilterName]] = '';
        }

        
        var link = searchFilters.find('#apply-filter');
        var newHref = urlConstructor(newArgs);
        link.attr('href', newHref);
    };

    searchFilters.find('#filter-behaviour').select2({
        minimumResultsForSearch: Infinity
    });
    searchFilters.find('#filter-comparision').select2({
        minimumResultsForSearch: Infinity
    });
    searchFilters.find('#filter-type').select2({
        minimumResultsForSearch: Infinity
    });
    searchFilters.find('.filter-value-picker').select2();
    searchFilters.on('select2:select', function () {
        showValuePicker();
        updateAddLink();
    });

    showValuePicker();
    updateRemoveLinks();
    updateAddLink();
});