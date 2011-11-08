from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.visits.models import Visit
from osp.visits.forms import VisitForm

@login_required
def log(request, user_id):
    template = 'visits/log.html'

    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)

    if request.user.groups.filter(name='Counselors'):
        can_privatize = True
    else:
        can_privatize = False

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.student = student
            visit.submitter = request.user
            visit.save()

            return HttpResponse(json.dumps({'status': 'success'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'template': render_to_string(template, {
                    'form': form,
                    'student': student,
                    'can_privatize': can_privatize}, RequestContext(request))
            }), content_type='application/json')
    else:
        form = VisitForm()

        return direct_to_template(request, template, {
            'form': form,
            'student': student,
            'can_privatize': can_privatize})

@login_required
def view(request, user_id, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    if (not request.user.groups.filter(name='Employees')
        or (visit.private
            and not request.user.groups.filter(name='Counselors'))):
        raise Http403

    return direct_to_template(request, 'visits/view.html', {
        'visit': visit})

@login_required
def view_all(request, user_id, page):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)

    visits = Visit.objects.filter(student=student)
    if not request.user.groups.filter(name='Counselors'):
        visits = visits.filter(private=False)

    page = int(page)
    paginator = Paginator(visits, 5)
    if page > paginator.num_pages:
        page = paginator.page(paginator.num_pages)
    elif page < 1:
        page = paginator.page(1)
    else:
        page = paginator.page(page)
    visits = page.object_list

    return direct_to_template(request, 'visits/view_all.html', {
        'visits': visits,
        'page': page,
        'paginator': paginator})
