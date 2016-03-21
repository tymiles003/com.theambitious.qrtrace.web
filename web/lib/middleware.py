import re
from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from web.member.models import MemberPayment
from web.campaign.models import Campaign



class CheckSubscription(object):
    def process_request(self, request):

        if request.user.is_authenticated() and request.method!='POST' and not request.is_ajax():
            m = messages.get_messages(request)
            if len(m) == 0:
                try:
                    mp = MemberPayment.objects.filter(user=request.user, end_at__gt=datetime.now())[0:1].get()
                        
                except:
                    cc = Campaign.objects.filter(user=request.user, campaign_type='P').count()
                    if cc > 0:
    
                            messages.error(request, 'Your Mini-Sites are not active because your subscription expired. click "My Account" to renew')     
        