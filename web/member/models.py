from django.db import models
from django.contrib.auth.models import User


class MemberPayment(models.Model):
    user = models.ForeignKey(User, db_index=True)
    memo = models.CharField(max_length=255,)
    amount = models.DecimalField(max_digits=5, decimal_places=2,)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
