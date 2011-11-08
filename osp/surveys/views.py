from django.contrib.auth.decorators import login_required
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.surveys.forms import SurveyForm
from osp.surveys.models import Result, Answer

@login_required
def survey(request):
    if not request.user.groups.filter(name='Students'):
        raise Http403

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            result = Result(student=request.user)
            result.save()
            for question, ans in request.POST.items():
                field = form.fields.get(question)
                if field:
                    answer = Answer(result=result)
                    answer.order = question.split('_')[1]
                    answer.question = field.label
                    # There has to be a better way to check this
                    if isinstance(field.widget, CheckboxSelectMultiple):
                        ans = ', '.join(request.POST.getlist(question))
                    answer.answer = ans
                    answer.save()
            return redirect('profile:profile', request.user.id)
    else:
        form = SurveyForm()

    return direct_to_template(request, 'surveys/survey.html', {'form': form})

@login_required
def results(request, result_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    result = get_object_or_404(Result, pk=result_id)

    if (not request.user.groups.filter(name='Employees') and
        result.student != request.user):
        raise Http403

    return direct_to_template(request, 'surveys/results.html',
        {'result': result})
