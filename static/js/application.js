$(function () {
    $('form.form-danger').submit(function () {
        return confirm($(this).data('confirm'));
    });

    $('.selectpicker').selectpicker({
        'selectedText': 'cat',
    });
});
