var EditableCell = (function (){
    var klass = function EditableCell($el) {
        this.$el = $el;
        this.listenClick();
    }

    klass.prototype.listenClick = function () {
        var self = this
        this.$el.find('.switch-edit').on('click', function (ev) {
            self.toggle();
            return false;
        });
    }

    klass.prototype.toggle = function () {
        this.$el.find('.editable-cell-info, .editable-cell-edit').toggle();
    }

    return klass;
}());

$(function () {
    $('form.form-danger').submit(function () {
        return confirm($(this).data('confirm'));
    });

    $(".click-confirm").click(function(){
      if(confirm($(this).data('confirm'))){
        eval($(this).data('success'));
      }
    });

    $('.selectpicker').selectpicker({
        'selectedText': 'cat',
    });

    $('.editable-cell').each(function () {
        window.lastcell = new EditableCell($(this));
    });
});
