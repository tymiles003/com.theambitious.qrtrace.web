from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()



@register.filter
def form_errors(errors, autoescape=None):
    """Format form-level error messages."""
    esc = lambda x: x
    if autoescape:
        esc = conditional_escape

    new_html = ''
    for error in errors:
        new_html += '<div class="alert-message error">'
        new_html += '  <a class="close" href="#">&times;</a>'
        new_html += '  <p>%s</p>' % esc(str(error))
        new_html += '</div>'
    return mark_safe(new_html)
form_errors.needs_autoescape = True


@register.filter
def field_errors(field_errors, extra=None):
    """Format the field-level error messages."""
    html = ''
    if field_errors:
        if extra == "newline":
            html += '<br />'
        html += '<span class="help-inline">'
        html += ' '.join(map(str, field_errors))
        html += '</span>'
        return mark_safe(html)
    return ''
