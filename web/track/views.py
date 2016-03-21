from django.shortcuts import  redirect, render_to_response
from web.campaign.models import Campaign, Scan, Premium
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from web.lib.json import JsonResponse
from datetime import datetime
from web.campaign.models import Note
from web.campaign.forms import NoteForm,ClickForm
from web.member.models import MemberPayment


def save_click(request):
    data = { 'success': False }
    if request.is_ajax():
        if request.method == 'POST':
            user_agent = ''
            refer = ''
            ip = ''
            
            try:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            except:
                ip = request.META['REMOTE_ADDR']
                
            if 'HTTP_REFERER' in request.META:
                refer = request.META['HTTP_REFERER']
            
            if 'HTTP_USER_AGENT' in request.META:
                user_agent = request.META['HTTP_USER_AGENT']
            
            posted = request.POST.copy()
            posted['ip'] = ip
            posted['user_agent'] = user_agent
            posted['refer'] = refer         
            form = ClickForm(posted)
            if form.is_valid():
                form.save()
                data = { 'success': True }
            
    return JsonResponse(False, data=data)


def save_note(request):
    data = { 'success': False }
    if request.is_ajax():
        form = NoteForm()
        if request.method == 'POST':
            user_agent = ''
            refer = ''
            ip = ''
            
            try:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            except:
                ip = request.META['REMOTE_ADDR']
                
            if 'HTTP_REFERER' in request.META:
                refer = request.META['HTTP_REFERER']
            
            if 'HTTP_USER_AGENT' in request.META:
                user_agent = request.META['HTTP_USER_AGENT']
            
            posted = request.POST.copy()
            posted['ip'] = ip
            posted['user_agent'] = user_agent
            posted['refer'] = refer         
            form = NoteForm(posted)
            if form.is_valid():
                form.save()
                data = { 'success': True }
            
    return JsonResponse(False, data=data)


    pass

def track(request):
    c = None
    ps = None
    
    if 'c' in request.GET:
        refer = ''
        user_agent = ''
        campaign_id = int(request.GET['c'])
        try:
            c = Campaign.objects.get(id=campaign_id, status='A')
        except:
            return None
        
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            ip = request.META['REMOTE_ADDR']
        if 'HTTP_REFERER' in request.META:
            refer = request.META['HTTP_REFERER']
        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']
        
        if 'c_' + str(c.id) in request.session:
            pass
        else:
            s = Scan(campaign=c, ip=ip, refer=refer, user_agent=user_agent)
            s.save()
        
        if 'c_' + str(c.id)  not in request.session:
            request.session['c_' + str(c.id)] = 1
            
        if c.campaign_type == 'P':
            try:    
                mp = MemberPayment.objects.filter(user=c.user, end_at__gt=datetime.now()).order_by('-id')[0:1].get()
            except:
                return redirect(c.data)
            
            ps = Premium.objects.filter(campaign=c).order_by('seq')
            
        elif '://' in c.data:
            return redirect(c.data)
    
    return render_to_response('track/track.html', 
                              {'c':c,
                               'ps':ps, },
                              context_instance=RequestContext(request))     