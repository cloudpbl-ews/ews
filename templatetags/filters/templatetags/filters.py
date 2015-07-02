from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_alert_class(value):
    key_dict = {
        'success': 'alert-success',
        'info': 'alert-info',
        'warning': 'alert-warning',
        'error': 'alert-danger',
    }
    return key_dict[value]

@register.assignment_tag
def get_vm_is_running(vm):
    return vm.is_running
