from django import forms
from django.conf import settings
from osp.rosters.models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ('students', 'date_submitted', 'staff', 'section')
