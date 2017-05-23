from django import template
from django.forms.widgets import (
    Select,
    SelectMultiple,
    CheckboxInput,
    CheckboxSelectMultiple,
    Input,
)
register = template.Library()


def _checkbox_layout():
    return '''
    <div class="checkbox">
        <label for="{id}">{input}{label}</label>
        <p class="help-block">{help}</p>
    </div>
    '''


def _checkbox_multiple_layout(widget):
    print(dir(widget))
    print(next(widget.subwidgets(None, None)))
    layout = ''
    for value in widget.subwidgets(None, None):
        print(dir(value))
        layout += '<div class="checkbox">'+value.render()+'</div>'
    return layout


@register.filter
def bootstrap(value):

    layout = '''
    {tag}
    <div class="form-group">
        <label for="{id}">{label}</label>
        {input}
        <p class="help-block">{help}</p>
    </div>
    '''

    widget = value.field.widget
    if type(widget) in (Select, SelectMultiple, Input):
        value.field.widget.attrs['class'] = 'form-control'
    elif type(widget) == CheckboxInput:
        value.field.widget.attrs['class'] = 'checkbox'
        layout = _checkbox_layout()
    elif type(widget) == CheckboxSelectMultiple:
        return _checkbox_multiple_layout(widget)

    return layout.format(
        tag=value.field.widget,
        label=value.label,
        id=value.id_for_label,
        input=value,
        help=value.help_text
    )
