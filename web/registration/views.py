from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from web.registration.forms import StdRegForm
from _mysql_exceptions import IntegrityError
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from web.campaign.models import Campaign
from django.contrib.auth import authenticate, login as user_login
from web.registration.forms import P1RegForm, P2RegForm, PRegForm
import json
from django.forms.utils import ErrorList
from web.member.models import MemberPayment
from web.campaign.models import Premium


def standard(request):
    
    form = StdRegForm()
    if request.method == 'POST':
        form = StdRegForm(request.POST)
        if form.is_valid():
            uc = User.objects.filter(email=form.cleaned_data['email']).count()
            if(uc > 0):
                messages.error(request, 'There is already an account registered with this email')
                new_user = None
            else:
                new_user = User(
                  email=form.cleaned_data['email'],
                  username=form.cleaned_data['email'],
                  password = form.cleaned_data['password'],
                  last_login=datetime.now(),
                  is_staff=False,
                  is_superuser=False,)

                new_user.set_password(form.cleaned_data['password'])
                try:
                    new_user.save()
                    new_user.username = new_user.id
                    new_user.save()
                except IntegrityError:
                    messages.error(request, 'There is already an account registered with this email')
                    new_user = None

            if new_user:

                auth_user = authenticate(username=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'])

                if auth_user is not None:
                    if auth_user.is_active:
                        user_login(request, auth_user)
                        c = Campaign(user=auth_user, name=form.cleaned_data['name'], status='A')
                        c.save()    
                        messages.success(request, 'Your campaign has been created!')
                        return redirect(reverse('web.member.views.dash'))

                
    return render_to_response('registration/standard.html', 
                              {'form':form},
                              context_instance=RequestContext(request))


def premium(request, campaign_id=None):
    if campaign_id:
        try:
            c = Campaign.objects.get(user=request.user, id=campaign_id, campaign_type='P')
        except:
            return redirect(reverse('web.general.views.home'))
        
        #sessioned = request.session
        #for k,v in sessioned:
            
            #if 'preview_' in k:
                
                #del request.session[k]
        request.session['preview_campaign_id'] = c.id
        request.session['preview_title'] = c.premium_title
        request.session['preview_url'] = c.data
        request.session['preview_campaign_name'] = c.name
        form = P1RegForm(initial={'title':c.premium_title, 'data': c.data, 'campaign_name':c.name})
        
    else:      
        form = P1RegForm()
        
    if request.method == 'POST':

        form = P1RegForm(request.POST)
        if form.is_valid():
            request.session['preview_title'] = form.cleaned_data['title']
            request.session['preview_campaign_name'] = form.cleaned_data['campaign_name']
            request.session['preview_url'] = form.cleaned_data['url']
            if 'preview_link' not in request.session or ('preview_link' in request.session and request.session['preview_link'] == '{}'):
                messages.error(request, 'You must select at least one link.')
            else:
                return redirect(reverse('web.registration.views.premium_next'))
    return render_to_response('registration/premium.html', 
                              {'form':form},
                              context_instance=RequestContext(request))


def premium_next(request):
    if 'preview_campaign_name' not in request.session  or 'preview_title' not in request.session or 'preview_url' not in request.session or 'preview_link' not in request.session:
        return redirect(reverse('web.registration.views.premium'))
    
    c = None
    ps = None
    if 'preview_campaign_id' in request.session:
        try:
            c = Campaign.objects.get(user=request.user, id=request.session['preview_campaign_id'], campaign_type='P')

            ps = Premium.objects.filter(campaign = c)
            print(ps)
        except:
            return redirect(reverse('web.general.views.home'))
        
    pl = json.loads(request.session['preview_link'])
    
    tw = None
    fb = None
    for l in pl:
        if pl[l] == 'TW':
            tw = True 
        elif pl[l] == 'FB':
            fb = True
        elif pl[l] == 'WEB':
            #set web url from previous form submission
            request.session['preview_WEB'] = request.session['preview_url']
    try:
        mp = MemberPayment.objects.filter(user=request.user, end_at__gt=datetime.now()).order_by('-id')[0:1].get()
    except:
        mp = None
    if not fb and not tw:
        
        if request.user.is_authenticated() and mp:
            #create campaign

            return redirect(reverse('web.registration.views.premium_create_campaign'))
            
        elif request.user.is_authenticated() and not mp:
            #upgrade
            return redirect(reverse('web.registration.views.premium_upgrade_account'))
        else:
            #create account
            return redirect(reverse('web.registration.views.premium_create_account'))
        pass
    
    
    if ps:
        initial = {}
        for p in ps:
            if p.name == 'TW':
                initial['TW'] = p.val
            elif p.name == 'FB':
                initial['FB'] = p.val
        form = P2RegForm(initial=initial)
    else:
        form = P2RegForm()
    if request.method == 'POST':
        form = P2RegForm(request.POST)
        if form.is_valid():
            invalid = None
            if 'TW' in request.POST:
                if request.POST['TW'] == '':
                    invalid = True
                    form._errors['TW'] = ErrorList([u"Required Field"])
            if 'FB' in request.POST:
                if request.POST['FB'] == '':
                    invalid = True
                    form._errors['FB'] = ErrorList([u"Required Field"])
                    
            if not invalid:
                request.session['preview_TW'] = form.cleaned_data['TW']
                request.session['preview_FB'] = form.cleaned_data['FB']
                
                try:
                    mp = MemberPayment.objects.filter(user=request.user, end_at__gt=datetime.now()).order_by('-id')[0:1].get()
                except:
                    mp = None
                if request.user.is_authenticated() and mp:
                    #create campaign
                    return redirect(reverse('web.registration.views.premium_create_campaign'))
                    
                elif request.user.is_authenticated() and not mp:
                    #upgrade
                    return redirect(reverse('web.registration.views.premium_upgrade_account'))
                    
                else:
                    #create account
                    return redirect(reverse('web.registration.views.premium_create_account'))
                    
        else:
            pass
    return render_to_response('registration/premium_next.html', 
                              {'form':form,
                               'tw':tw,
                               'fb':fb},
                              context_instance=RequestContext(request))


def premium_create_account(request):
    if 'preview_campaign_name' not in request.session  or 'preview_title' not in request.session or 'preview_url' not in request.session or 'preview_link' not in request.session:
        return redirect(reverse('web.registration.views.premium'))
    
    if request.user.is_authenticated():
        return redirect(reverse('web.member.views.dash'))
    form = PRegForm()
    if request.method == 'POST':
        form = PRegForm(request.POST)
        if form.is_valid():
            new_user = User(
                  email=form.cleaned_data['email'],
                  username=form.cleaned_data['email'],
                  password = form.cleaned_data['password'],
                  last_login=datetime.now(),
                  is_staff=False,
                  is_superuser=False,)

            new_user.set_password(form.cleaned_data['password'])        
            try:
                new_user.save()
                new_user.username = new_user.id
                new_user.save()
            except IntegrityError:
                messages.error(request, 'There is already an account registered with this email')
                form.add_unique_email_error()
                new_user = None            
            
            if new_user:

                auth_user = authenticate(username=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'])

                if auth_user is not None:
                    if auth_user.is_active:
                        user_login(request, auth_user)

                                              
                        
                        mp = MemberPayment(user=auth_user, memo='30 day trial', amount=str(0.00), start_at=datetime.now(), end_at = (datetime.now() + timedelta(days=30)))
                        mp.save()
                                             
                        return redirect(reverse('web.registration.views.premium_create_campaign'))
    return render_to_response('registration/premium_create_account.html', 
                              {'form':form},
                              context_instance=RequestContext(request))


def premium_create_campaign(request):
    if 'preview_campaign_name' not in request.session  or 'preview_title' not in request.session or 'preview_url' not in request.session or 'preview_link' not in request.session:
        return redirect(reverse('web.registration.views.premium'))
    
    if not request.user.is_authenticated():
        return redirect(reverse('web.member.views.dash'))
    
    pl = json.loads(request.session['preview_link']) 
    premium_title = ''
    premium_theme = ''
    premium_header_theme = ''
    
    if 'preview_title' in request.session:
        premium_title = request.session['preview_title']
    
    if 'preview_theme' in request.session:
        premium_theme = request.session['preview_theme']
    else:
        premium_theme = 'a'
        
    if 'preview_header_theme' in request.session:
        premium_header_theme = request.session['preview_header_theme']
    else:
        premium_header_theme = 'a'    
    c = Campaign(user=request.user, name=request.session['preview_campaign_name'], campaign_type='P', status='A', data=request.session['preview_url'], premium_title=premium_title, premium_theme=premium_theme, premium_header_theme=premium_header_theme)
    
    c.save()     
    for l in pl:
        if 'preview_' + pl[l] in request.session:
            val = request.session['preview_' + pl[l]]
        else:
            val = ''
        seq = l
        name = pl[l]
        if name != '':
            storage = messages.get_messages(request)
            storage.used = True

            p = Premium(campaign=c, name=name, val=val, seq=seq)
            p.save()
    return redirect(reverse('web.member.views.campaign_details', args=[c.id]))

    return render_to_response('registration/premium_create_campaign.html', 
                              {},
                              context_instance=RequestContext(request))


def premium_upgrade_account(request):
    
    
    mp_check = MemberPayment.objects.filter(user=request.user).count()
    if mp_check == 0:
        mp = MemberPayment(user=request.user, memo='30 day trial', amount=str(0.00), start_at=datetime.now(), end_at = (datetime.now() + timedelta(days=30)))
        mp.save()
        messages.success(request, "Congrats. Your account has been upgraded.")
        return redirect(reverse('web.registration.views.premium_create_campaign'))
    else:
        messages.error(request, "You must purchase a Mini-Site Subscription to continue")
        return redirect(reverse('web.member.views.account'))
    return render_to_response('registration/premium_upgrade_account.html', 
                              {},
                              context_instance=RequestContext(request))
   