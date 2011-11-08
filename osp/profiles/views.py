from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.lib import jungian
from osp.core.middleware.http import Http403
from osp.visits.models import Visit

@login_required
def profile(request, user_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    student = get_object_or_404(User, pk=user_id, groups__name='Students')

    # Make sure the logged-in user should have access to this profile
    if (not request.user.groups.filter(name='Employees')
        and student != request.user):
        raise Http403

    current_enrollments = student.enrollment_set.filter(
        status__in=settings.ACTIVE_ENROLLMENT_STATUSES,
        section__term=settings.CURRENT_TERM,
        section__year__exact=settings.CURRENT_YEAR)

    try:
        latest_personality_type_result = (
            student.personalitytyperesult_set.latest('date_taken'))
    except:
        latest_personality_type_result = None
    try:
        latest_learning_style_result = (
            student.learningstyleresult_set.latest('date_taken'))
    except:
        latest_learning_style_result = None

    if latest_personality_type_result:
        personality_type_analysis = jungian.TypeAnalysis(
            args=json.loads(latest_personality_type_result.answers),
            likert=4,
            scale=100)
        personality_type_scores = [
            (score[0], score[1], (1 - score[1]))
            for score in personality_type_analysis.graphScores]
    else:
        personality_type_scores = None

    if (not request.user.groups.filter(name='Counselors')
        and not request.user.groups.filter(name='Instructors')):
        can_view_visits = False
        visits = None
    else:
        can_view_visits = True
        visits = Visit.objects.filter(student=student)

        if not request.user.groups.filter(name='Counselors'):
            visits = visits.filter(private=False)

    if visits:
        paginator = Paginator(visits, 5)
        page = paginator.page(1)
        visits = page.object_list
    else:
        paginator = False
        page = False


    return direct_to_template(request, 'profiles/profile.html', {
        'student': student,
        'current_enrollments': current_enrollments,
        'latest_personality_type_result': latest_personality_type_result,
        'personality_type_scores': personality_type_scores,
        'latest_learning_style_result': latest_learning_style_result,
        'can_view_visits': can_view_visits,
        'visits': visits,
        'paginator': paginator,
        'page': page,
    })
