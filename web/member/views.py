from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from web.campaign.models import Campaign, Scan, Click
from django.db.models.aggregates import Count
from datetime import timedelta
from datetime import datetime, time, date
from django.http import HttpResponse
import csv
from web.member.forms import ChangePasswordForm
from web.member.models import MemberPayment
from web.campaign.forms import NewStdCampaignForm
from dateutil.relativedelta import relativedelta
from web.campaign.models import PCAMPAIGN_LINK_TEXT_LOOKUP,  Note


@login_required
def dash(request):
    cs = Campaign.objects.filter(user=request.user).order_by('-updated_at')[0:5]
    return render_to_response('member/dash.html', 
                              {'cs':cs},
                              context_instance=RequestContext(request))


@login_required
def campaign(request, campaign_type = None):
        
    count_list = []
    if campaign_type == 'S' or campaign_type == 'P':
        cs = Campaign.objects.filter(user=request.user, campaign_type=campaign_type).order_by('name')
    elif not campaign_type:
        cs = Campaign.objects.filter(user=request.user).order_by('name')
    else:
        return redirect(reverse('web.general.views.home'))
    
    for c in cs:
        count_list.append(c.id)
    dt = datetime.today()
    d = date(dt.year, dt.month, dt.day)
    t = time(0,0)
    
    ss = Scan.objects.extra(select={'campaign': 'campaign_id'}).values('campaign').filter(campaign__in=count_list, created_at__gte=datetime.combine(d,t)).annotate(c=Count('campaign'))
    ss_dict = {}
    for s in ss:
        ss_dict[s['campaign']] = s['c']
    for c in cs:
        if c.id in ss_dict:
            c.d_day_count = ss_dict[c.id]
        else:
            c.d_day_count = 0
    return render_to_response('member/campaign.html', 
                              {'cs':cs,
                              },
                              context_instance=RequestContext(request))


@login_required
def campaign_details(request, campaign_id):
    ccs = None
    notes = None
    try:
        c = Campaign.objects.get(user=request.user, id=campaign_id)
        
    except:
        return redirect(reverse('web.general.views.home'))

    ss = Scan.objects.extra(select={'day': 'date( created_at )'}).values('day').filter(campaign=c).annotate(c=Count('created_at')).order_by('-day')
    current_day = datetime.now()
    days = {}
    for n in [0,1,2,3,4,5,6]:
        cd = current_day - timedelta(days=n)
        days[cd.strftime('%m-%d')] = 0 
    chart_data_x = ''
    chart_data_y = ''
    
    for s in ss:
        if s['day'].strftime("%m-%d") in days:
            days[s['day'].strftime("%m-%d")] = s['c']
    
    counter = len(days)
    for k in sorted(days.iterkeys(), reverse=True):   
        chart_data_x = chart_data_x + '[' + str((counter)) + ',"' + str(k) + '"], '
        chart_data_y = chart_data_y + '[' + str((counter)) + ',' + str(days[k]) + '], '
        
        counter -= 1
    if c.campaign_type == 'P':
        ccs = Click.objects.extra().values('click_type').filter(campaign=c).annotate(c=Count('created_at'))
        notes = Note.objects.filter(campaign=c).order_by('-id')
        total = 0
        for cc in ccs:
            cc['d_click_type'] = PCAMPAIGN_LINK_TEXT_LOOKUP[cc['click_type']]
            total = total + cc['c']
        for cc in ccs:
            if total == 0:
                cc['d_click_percent'] = 0
            else:
                cc['d_click_percent'] = int((float(cc['c']) / float(total))*100)
        
    return render_to_response('member/campaign_details.html', 
                              {'c':c,
                               'ss':ss,
                               'ccs':ccs,
                               'notes': notes,
                               'chart_data_x': chart_data_x,
                               'chart_data_y': chart_data_y},
                              context_instance=RequestContext(request))


@login_required
def campaign_new_edit(request, campaign_id=None):
    try:
        mp = MemberPayment.objects.filter(user=request.user, end_at__gt=datetime.now()).order_by('-id')[0:1].get()    
    except:
        mp = None    
     
    c = None   
    if campaign_id:
        try:
            c = Campaign.objects.get(user=request.user, id=campaign_id)
            form = NewStdCampaignForm(instance=c)
        except:
            return redirect(reverse('web.general.views.home'))
    else:
        form = NewStdCampaignForm()
        
    if request.method == 'POST':
        posted = request.POST.copy()
        posted['user'] = request.user.id
        posted['campaign_type'] = 'S'
        
        if campaign_id:
            form = NewStdCampaignForm(posted, instance=c)
        else:
            form = NewStdCampaignForm(posted)
        if form.is_valid():
            if c:
                messages.success(request, 'Your campaign was edited.')
            else:
                messages.success(request, 'A new campaign was created.')

            c = form.save()
            
            return redirect(reverse('web.member.views.campaign_details', args=[c.id]))
    return render_to_response('member/campaign_new_edit.html', 
                              {'form':form,
                               'c':c,
                               'mp':mp},
                              context_instance=RequestContext(request))


@login_required
def campaign_export(request, campaign_id):
    try:
        c = Campaign.objects.get(user=request.user, id=campaign_id)
    except:
        return redirect(reverse('web.general.views.home'))
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=qrtrace_' + str(c.id) + '_' + datetime.now().strftime('%Y%m%d') + '.csv'
    writer = csv.writer(response)

    ss = Scan.objects.filter(campaign=c)
    writer.writerow(['ID', 'IP Address', 'Refer URL', 'User Agent', 'Created at'])
    
    for s in ss:
        writer.writerow([s.id, s.ip, s.refer, s.user_agent, s.created_at])

    return response
               
                 
@login_required                 
def account(request):
    mp_old = MemberPayment.objects.filter(user=request.user, end_at__lte=datetime.now()).count()
    try:    
        mp = MemberPayment.objects.filter(user=request.user, end_at__gt=datetime.now()).order_by('-id')[0:1].get()
    except:
        mp = None
    cp_form = ChangePasswordForm(instance=request.user)
    if request.method == 'POST':
        if 'password' in request.POST:
            cp_form = ChangePasswordForm(request.POST, instance=request.user)
            if cp_form.is_valid():
                request.user.set_password(cp_form.cleaned_data['password'])
                request.user.save()
                #log_profile_updated(request.user)
                messages.success(request, 'Yay. You have changed your password!')      
                return redirect(reverse('web.member.views.account'))
    return render_to_response('member/account.html', 
                              {'cp_form': cp_form,
                               'mp': mp,
                               'mp_old': mp_old},
                              context_instance=RequestContext(request))

@login_required
def thanks(request):
    mp = None
    if 'HTTP_REFERER' not in request.META:
        refer = request.META['HTTP_REFERER']
        if 'paypal' not in refer:
            date_start = None
            date_end = None
            try:
                mp_check = MemberPayment.objects.filter(user=request.user).order_by('-end_at')[0:1].get()
                if mp_check:
                    date_start = mp_check.end_at 
                    date_end = date_start + relativedelta(years=1)
                    
            except:        
                date_start = datetime.now()
                date_end = datetime.now() + relativedelta(years=1)
            
            mp = MemberPayment(user=request.user, memo='1 year payment', amount=str(40.00), start_at=date_start, end_at=date_end)
            mp.save()            
        
    return render_to_response('member/thanks.html', 
                              {'mp':mp},
                              context_instance=RequestContext(request))


@login_required         
def log_out(request):
    logout(request)
    return redirect(reverse('web.general.views.home'))