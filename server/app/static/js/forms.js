$(function () {
    $('form').on('submit', function (e) {
        e.preventDefault();
        $('#submit-btn').prop('disabled', true).val('Procesando...');
        NProgress.start()
        var form = this;
        setTimeout(function () {
            form.submit();
        }, 100)
        return false;
    });
});