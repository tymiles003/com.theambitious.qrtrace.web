from django.conf import settings


def site_url(request):
    return {'SITE_URL': settings.STATIC_URL}


def add_session(request):
    return {'session': request.session}


def server_type(request):
    return {'SERVER_TYPE': settings.SERVER_TYPE}
