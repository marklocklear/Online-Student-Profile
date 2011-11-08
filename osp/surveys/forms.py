import os

from django import forms
from django.utils import simplejson as json

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(APP_ROOT, 'data')

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)

        f = file(os.path.join(DATA_ROOT, 'survey_questions.json'))
        data = f.read()
        data = json.loads(data)
        f.close()

        i = 1
        for question in data:
            label = question['question']
            if question.has_key('answers'):
                choices = [(x, x) for x in question['answers']]

            if question['type'] == 'text':
                field = forms.CharField(label=label, required=False)
            elif question['type'] == 'select':
                choices.insert(0, ('', ''))
                field = forms.ChoiceField(label=label, choices=choices,
                    required=False)
            elif question['type'] == 'radio':
                field = forms.ChoiceField(label=label, choices=choices,
                    widget=forms.RadioSelect, required=False)
            elif question['type'] == 'checkbox':
                field = forms.MultipleChoiceField(label=label, choices=choices,
                    widget=forms.CheckboxSelectMultiple, required=False)

            self.fields['question_%d' % i] = field
            i += 1
