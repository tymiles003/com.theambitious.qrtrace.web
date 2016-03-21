from datetime import date, datetime
from decimal import Decimal

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from simplejson import dumps, loads, JSONEncoder


class DjangoJSONEncoder(JSONEncoder):
    """http://stackoverflow.com/questions/2249792/json-serializing-django-models-with-simplejson"""

    def __init__(self, round_decimal_places=2, *args, **kwargs):
        super(DjangoJSONEncoder, self).__init__(*args, **kwargs)
        self.round_decimal_places = round_decimal_places

    def default(self, obj):
        if isinstance(obj, QuerySet):
            # TODO - follow relations.
            # See: https://code.djangoproject.com/ticket/4656
            return loads(serialize('json', obj))
        elif isinstance(obj, Decimal):
            return ('%.' + str(self.round_decimal_places) + 'f') % obj
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%I:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return JSONEncoder.default(self, obj)


class JsonResponse(HttpResponse):
    """Encode the response as JSON."""

    def __init__(self, success, data=None, messages=None, round_decimal_places=2):
        self.round_decimal_places = round_decimal_places
        if success: 
            json_success = 'true'
        else:
            json_success = 'false'
        content = dumps( {
                         'success': json_success,
                         'data': data,
                         'messages': messages},
                        indent=2,
                        default=self.handler,
                        cls=DjangoJSONEncoder)
        
        super(JsonResponse, self).__init__(content=content,
                                           content_type='application/json')

    def handler(self, obj):
        if isinstance(obj, Decimal):
            return ('%.' + str(self.round_decimal_places) + 'f') % obj
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%I:%S')
        return JSONEncoder.default(self, obj)


def form_errors(form):
    """Pull all errors out of a form into a dictionary of arrays."""
    errors = {}
    for field in form:
        if field.errors:
            errors[field.name] = []
            for error in field.errors:
                errors[field.name].append(error)
    if '__all__' in form.errors:
        errors['__all__'] = []
        for error in form.errors['__all__']:
            errors['__all__'].append(error)
    return errors
