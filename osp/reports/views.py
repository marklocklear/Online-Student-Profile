from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.assessments.models import LearningStyleResult, PersonalityTypeResult
from osp.reports.forms import DateRangeForm
from osp.reports.utils import generate_xls_report

@login_required
def learning_styles_report(request):
    if (not request.user.groups.filter(name='Instructors')
        and not request.user.groups.filter(name='Counselors')):
        raise Http403

    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            results = LearningStyleResult.objects.filter(
                date_taken__range=(
                    datetime.combine(form.cleaned_data['from_date'], time.min),
                    datetime.combine(form.cleaned_data['to_date'], time.max),
                )
            )
            if results:
                filename = ('learning_styles-%s-%s.xls'
                            % (form.cleaned_data['from_date'].strftime('%Y%m%d'),
                               form.cleaned_data['to_date'].strftime('%Y%m%d')))
                columns = ('User Index', 'Student Username', 'Date Taken',
                           'Learning Styles', 'Kinesthetic', 'Visual', 'Auditory')
                rows = []
                for result in results:
                    row = (result.student.id,
                           result.student.username,
                           result.date_taken.strftime('%m/%d/%Y'),
                           result.learning_style,
                           result.kinesthetic_score,
                           result.visual_score,
                           result.auditory_score)
                    rows.append(row)

                return generate_xls_report(filename, 'Learning Styles Report', columns, rows)
        return direct_to_template(request, 'reports/report_form.html', {
            'error': True,
            'learning': True,
        })

    return direct_to_template(request, 'reports/report_form.html', {
        'learning': True,
    })

@login_required
def personality_type_report(request):
    if (not request.user.groups.filter(name='Instructors')
        and not request.user.groups.filter(name='Counselors')):
        raise Http403

    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            results = PersonalityTypeResult.objects.filter(
                date_taken__range=(
                    datetime.combine(form.cleaned_data['from_date'], time.min),
                    datetime.combine(form.cleaned_data['to_date'], time.max),
                )
            )
            if results:
                filename = ('personality_type-%s-%s.xls'
                            % (form.cleaned_data['from_date'].strftime('%Y%m%d'),
                               form.cleaned_data['to_date'].strftime('%Y%m%d')))
                columns = ('User Index', 'Student Username', 'Date Taken',
                           'Personality Type', 'First Category Score',
                           'Second Category Score', 'Third Category Score',
                           'Fourth Category Score')
                rows = []
                for result in results:
                    row = (result.student.id,
                           result.student.username,
                           result.date_taken.strftime('%m/%d/%Y'),
                           result.personality_type,
                           result.first_category_score,
                           result.second_category_score,
                           result.third_category_score,
                           result.fourth_category_score)
                    rows.append(row)

                return generate_xls_report(filename, 'Personality Type Report', columns, rows)

        return direct_to_template(request, 'reports/report_form.html', {
            'error': True,
        })

    return direct_to_template(request, 'reports/report_form.html', {})
