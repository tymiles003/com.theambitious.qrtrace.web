from django.template import RequestContext
from django.shortcuts import render_to_response
from web.campaign.models import PCAMPAIGN_LINK_TEXT_LOOKUP
from web.lib.json import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def set_preview(request):
    data = {'success': False}
    if request.is_ajax():
        if request.method == 'POST':
            
            if 'preview_title' in request.POST and request.POST['preview_title'] != '':
                request.session['preview_title'] = request.POST['preview_title']

            if 'preview_campaign_name' in request.POST and request.POST['preview_campaign_name'] != '':
                request.session['preview_campaign_name'] = request.POST['preview_campaign_name']           

            if 'preview_url' in request.POST and request.POST['preview_url'] != '':
                request.session['preview_url'] = request.POST['preview_url']       
                            
            if 'preview_theme' in request.POST and request.POST['preview_theme'] != '':
                request.session['preview_theme'] = request.POST['preview_theme']
            else:
                if 'preview_theme' in request.session:        
                    del request.session['preview_theme']            
            
            if 'preview_header_theme' in request.POST and request.POST['preview_header_theme'] != '':
                request.session['preview_header_theme'] = request.POST['preview_header_theme']
            else:
                if 'preview_header_theme' in request.session:
                    del request.session['preview_header_theme']
            if 'preview_link' in request.POST:
                request.session['preview_link'] = request.POST['preview_link']
                
            data = {'success': True}
    return JsonResponse(False, data=data)

def preview(request):
    display = {}
    if 'preview_link' in request.session:
        pl = json.loads(request.session['preview_link'])
        
        for k in pl:
            if pl[k] in PCAMPAIGN_LINK_TEXT_LOOKUP:
                display[k] = PCAMPAIGN_LINK_TEXT_LOOKUP[pl[k]]
    
    return render_to_response('campaign/preview.html', 
                              {'display':sorted(display.iteritems())},
                              context_instance=RequestContext(request))