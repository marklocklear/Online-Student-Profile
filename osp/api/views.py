from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from osp.api.utils import validate_credentials, load_users
from osp.core.models import UserProfile, Section, Enrollment

@csrf_exempt
def import_instructors(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0]['api_key'])

        # Load users into local database using utility method
        stats = load_users(data[0]['instructors'], ['Instructors', 'Employees'])

        status.append('Received %d instructor records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_students(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0]['api_key'])

        # Load users into local database using utility method
        stats = load_users(data[0]['students'], ['Students'])

        status.append('Received %d student records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_sections(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0].get('api_key', ''))

        # Redefine data variable to the actual section list
        data = data[0]['sections']

        # Let's keep a count of how many new and updated objects we have
        sections_updated = 0
        sections_created = 0

        # Grab all existing sections and users as well as their associated
        # objects from the database
        all_sections = Section.objects.filter(
            term=settings.CURRENT_TERM,
            year=settings.CURRENT_YEAR)
        all_users = UserProfile.objects.filter(
            user__groups__name='Instructors'
        ).select_related()

        for s in data:
            # Get the existing section object or create a new one
            new_section = False
            try:
                section = all_sections.filter(prefix=s['prefix'],
                                              number=s['number'],
                                              section=s['section'])[0]
            except IndexError:
                section = Section(prefix=s['prefix'],
                                  number=s['number'],
                                  section=s['section'],
                                  term=s['term'],
                                  year=s['year'])
                new_section = True

            # Increment counter for appropriate operation type
            if new_section:
                sections_created += 1
            else:
                sections_updated += 1

            # Only update metadata for section if changed
            if (section.title != s['title']
                or section.credit_hours != s['credit_hours']):
                section.title= s['title']
                section.credit_hours = s['credit_hours']

                section.save()
            elif new_section:
                section.save()

            # Clear existing instructors and add up-to-date list of
            # instructors to section
            section.instructors.clear()
            for i in s['instructors']:
                instructor_exists = True
                try:
                    instructor = all_users.filter(id_number=i)[0].user
                except IndexError:
                    status.append('Instructor (ID number %s) '
                                  'does not exist' % i)
                    instructor_exists = False

                if instructor_exists:
                    section.instructors.add(instructor)


        status.append('Received %d section records' % len(data))
        status.append('Updated %d section objects' % sections_updated)
        status.append('Created %d section objects' % sections_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_enrollments(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0].get('api_key', ''))

        # Redefine data variable to actual enrollment list
        data = data[0]['enrollments']

        # Let's keep a count of how many new and updated objects we have
        enrollments_updated = 0
        enrollments_created = 0

        # Grab all existing sections, users, and enrollments as well as
        # their associated objects from the database
        all_sections = Section.objects.filter(
            term=settings.CURRENT_TERM,
            year=settings.CURRENT_YEAR)
        all_users = UserProfile.objects.filter(
            user__groups__name='Students'
        ).select_related()
        all_enrollments = Enrollment.objects.filter(
            section__term=settings.CURRENT_TERM,
            section__year__exact=settings.CURRENT_YEAR)

        for e in data:
            section_exists = True
            try:
                section = all_sections.filter(prefix=e['prefix'],
                                              number=e['number'],
                                              section=e['section'])[0]
            except IndexError:
                status.append('Section (%s%s-%s) does not exist' % (
                    e['prefix'],
                    e['number'],
                    e['section']))
                section_exists = False

            student_exists = True
            try:
                student = all_users.filter(id_number=e['student'])[0].user
            except IndexError:
                status.append('Student (ID number %s) '
                              'does not exist' % e['student'])
                student_exists = False

            if section_exists and student_exists:
                new_enrollment = False
                try:
                    enrollment = all_enrollments.filter(section=section,
                                                        student=student)[0]
                except IndexError:
                    enrollment = Enrollment(student=student, section=section)
                    new_enrollment = True

                if new_enrollment:
                    enrollments_created += 1
                else:
                    enrollments_updated += 1


                # Only update metadata for enrollment if changed
                if enrollment.status != e['status']:
                    enrollment.status = e['status']
                    enrollment.save()
                elif new_enrollment:
                    enrollment.save()

        status.append('Received %d enrollment records' % len(data))
        status.append('Updated %d enrollment objects' % enrollments_updated)
        status.append('Created %d enrollment objects' % enrollments_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')
