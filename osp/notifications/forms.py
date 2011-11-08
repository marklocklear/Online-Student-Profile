from django import forms
from django.conf import settings
from osp.notifications.models import Intervention, Contact

class InterventionForm(forms.ModelForm):
    reasons = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=settings.INTERVENTION_REASONS)

    class Meta:
        model = Intervention
        exclude = ('students', 'section', 'instructor',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('students', 'section', 'instructor',)
