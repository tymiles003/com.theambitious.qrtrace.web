"""Email auth backend.
EmailBackend adapted from the following:
http://djangosnippets.org/snippets/2463/
http://djangosnippets.org/snippets/1845/
http://www.micahcarrick.com/django-email-authentication.html
"""

from datetime import datetime, timedelta
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import hashlib

class EmailBackend(ModelBackend):
    """Authenticate with email or Facebook instead of username."""

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None, login_type='STANDARD', fb_access_token=None, session=None):
        if login_type == 'STANDARD':
            
            username = username.lower()
            if EmailValidator(username):
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return None
            else:
                # Only email addresses accepted.
                return None

            # Authenticate against auth_user.password, 
            # if that fails check against member_member.legacy_password (and convert if valid)    
            
            if user.check_password(password) or self.check_legacy_password(user, password):
                return user
      
                    
        return None

    def check_legacy_password(self, user, raw_password):
        # legacy password used:
        # salt=sha1(md5(password)
        # password=md5(password + salt)
        salt=hashlib.sha1(hashlib.md5(raw_password).hexdigest()).hexdigest()
        legacy_password = hashlib.md5(raw_password + salt).hexdigest();

        # Convert if to new password if valid.
        is_correct = (user.password == legacy_password)
        if is_correct:
            # Convert the password to the new, more secure format.
            user.set_password(raw_password)
            user.save()
        return is_correct    
