from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.core.models import Section
from osp.notifications.forms import InterventionForm, ContactForm

@login_required
def notify(request,
           notification_type='contact',
           template='notifications/contact.html'):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403

    section_id = (request.POST['section_id']
                  if request.method == 'POST'
                  else request.GET['section_id'])
    section = get_object_or_404(Section, id=int(section_id))

    if not section.instructors.filter(username=request.user.username):
        raise Http403

    students = []
    student_list = (request.GET.getlist('students')
                    if request.method == 'GET'
                    else request.POST.get('students').split(','))
    for student_id in student_list:
        students.append(get_object_or_404(User, id=int(student_id)))

    if not students:
        raise Http403

    if request.method == 'POST':
        if notification_type == 'contact':
            form = ContactForm(request.POST)
        elif notification_type == 'intervention':
            form = InterventionForm(request.POST)
        if form.is_valid():
            if notification_type == 'contact':
                contact = form.save(commit=False)
                contact.instructor = request.user
                contact.section = section
                contact.save()
                for student_id in request.POST['students'].split(','):
                    contact.students.add(get_object_or_404(User,
                                                           id=int(student_id)))

                contact.email_contact()
            elif notification_type == 'intervention':
                intervention = form.save(commit=False)
                intervention.instructor = request.user
                intervention.section = section
                intervention.reasons = ','.join(form.data.getlist('reasons'))
                intervention.save()
                for student_id in request.POST['students'].split(','):
                    intervention.students.add(get_object_or_404(
                        User, id=int(student_id)))

                intervention.email_intervention()

            return HttpResponse(json.dumps({'status': 'success'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'template': render_to_string(template, {
                    'form': form,
                    'section': section,
                    'students': students}, RequestContext(request))
            }), content_type='application/json')
    else:
        if notification_type == 'contact':
            form = ContactForm(initial={
                'subject': 'Official Correspondence for %s - %s' % (
                           section, section.title),
                'message': 'Dear Student,\n\n\n\nThanks,\n%s' % (
                           request.user.get_full_name())
            })
        elif notification_type == 'intervention':
            form = InterventionForm()

        return direct_to_template(request, template, {
            'form': form,
            'section': section,
            'students': students})
