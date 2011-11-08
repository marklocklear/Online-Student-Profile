from django import forms
from osp.visits.models import Visit

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        exclude = ('student', 'submitter',)

