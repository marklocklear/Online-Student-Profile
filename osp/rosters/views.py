from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.core.models import Section

@login_required
def roster(request, section_id):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403

    section = get_object_or_404(Section, id=section_id)

    if not section.instructors.filter(username=request.user.username):
        raise Http403

    students = []
    learning_style_counts = {'auditory': 0, 'kinesthetic': 0, 'visual': 0}
    for enrollment in section.get_active_enrollments():
        # Grab learning style and personality type for each student
        try:
            personality_type_result = (
                enrollment.student.personalitytyperesult_set.latest(
                    'date_taken'))
        except:
            personality_type_result = None
        try:
            learning_style_result = (
                enrollment.student.learningstyleresult_set.latest('date_taken'))
        except:
            learning_style_result = None

        personality_type = (personality_type_result.personality_type
                            if personality_type_result
                            else '')
        learning_style = (learning_style_result.learning_style
                          if learning_style_result
                          else '')

        students.append({
            'id': enrollment.student.id,
            'full_name': enrollment.student.get_full_name(),
            'personality_type': personality_type,
            'learning_style': learning_style,
        })

        # Calculate learning style totals for class
        if learning_style_result:
            styles = learning_style_result.learning_style.split(', ')
            for style in styles:
                learning_style_counts[style] += 1

    return direct_to_template(request, 'rosters/roster.html', {
        'section': section,
        'students': students,
        'learning_style_counts': learning_style_counts})
