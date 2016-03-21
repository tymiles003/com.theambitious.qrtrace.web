from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as user_login, logout
import qrcode, numpy as np
from django.conf import settings as settings
from web.member.forms import LoginForm
from web.campaign.models import Campaign
from django.contrib.sites.models import Site

def home(request):
    auth_user = None
    if request.user.is_authenticated():
        return redirect(reverse('web.member.views.dash'))

    if request.method == 'POST' and 'email' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_user = authenticate(username=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
        else:
            messages.error(request, 'Incorrect login')
        if auth_user is not None:
            if auth_user.is_active:
                user_login(request, auth_user)
                return redirect(reverse('web.general.views.home'))

    if request.method == 'POST' and 'data' in request.POST:
        request.session['data'] = request.POST['data']
        return redirect(reverse('web.registration.views.standard'))
    return render_to_response('general/home.html', 
                              {},
                              context_instance=RequestContext(request))

def qr(request):

    size = 8
    data = ''
    if 'size' in request.GET:
        size = int(request.GET['size'])
    if 'data' in request.GET:
        data = request.GET['data']
    if 'campaign_id' in request.GET:
        campaign_id = int(request.GET['campaign_id'])
        try:
            c = Campaign.objects.get(user=request.user, id=campaign_id)
            data = 'http://%s%s' % (Site.objects.get_current().domain, reverse('web.track.views.track') + '?c=' + str(c.id))
        except:    
            return redirect(reverse('web.general.views.home'))
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    response = HttpResponse(content_type="image/png")

    img.save(response, 'PNG')

    return response   