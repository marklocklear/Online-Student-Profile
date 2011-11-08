from django import forms

def create_answers_tuple(data):
    answers = []
    i = 0
    for answer in data:
        answers.append([i, answer])
        i += 1
    return answers

def build_survey_form(data):
    fields = {}

    i = 1
    for question in data:
        if question['type'] == 'text':
            field = forms.CharField(label=question['question'])
        elif question['type'] == 'select':
            choices = create_answers_tuple(question['answers'])
            field = forms.ChoiceField(label=question['question'],
                choices=choices)
        elif question['type'] == 'radio':
            choices = create_answers_tuple(question['answers'])
            field = forms.ChoiceField(label=question['question'],
                choices=choices, widget=forms.RadioSelect)
        elif question['type'] == 'checkbox':
            choices = create_answers_tuple(question['answers'])
            field = forms.MultipleChoiceField(label=question['question'],
                choices=choices, widget=forms.CheckboxSelectMultiple)

        fields['question_%d' % i] = field
        i += 1

    return type('SurveyForm', (forms.BaseForm,), {'base_fields': fields})
