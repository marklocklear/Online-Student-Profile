from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import linebreaks
from django.template.loader import render_to_string

from osp.core.models import Section
from osp.notifications.utils import email_user

class Intervention(models.Model):
    students = models.ManyToManyField(User)
    section = models.ForeignKey(Section)
    instructor = models.ForeignKey(User, related_name='submitted_interventions')
    reasons = models.CharField(max_length=255)
    campus = models.CharField(max_length=255, choices=settings.CAMPUS_CHOICES)
    comments = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def email_intervention(self):
        subject = render_to_string(
            'notifications/email/intervention_alert_subject.txt',
            {'intervention': self})
        message = render_to_string(
            'notifications/email/intervention_alert_message.html',
            {'intervention': self, 'reasons': self.reasons.split(',')})
        # Send referral to settings.INTERVENTIONS_EMAIL
        email_user(settings.SERVER_EMAIL,
                   settings.INTERVENTIONS_EMAIL,
                   self.instructor.email,
                   subject,
                   message)

        # Notify students that an intervention referral was submitted for them
        subject = render_to_string(
            'notifications/email/intervention_student_subject.txt',
            {'intervention': self})
        for student in self.students.all():
            if student.email:
                message = render_to_string(
                    'notifications/email/intervention_student_message.html',
                    {'student': student})
                email_user(settings.SERVER_EMAIL,
                           student.email,
                           None,
                           subject,
                           message)


class Contact(models.Model):
    students = models.ManyToManyField(User)
    section = models.ForeignKey(Section)
    instructor = models.ForeignKey(User, related_name='submitted_contacts')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def email_contact(self):
        # Send students the instructor's message
        for student in self.students.all():
            if student.email:
                message = linebreaks(self.message)
                email_user(self.instructor.email,
                           student.email,
                           None,
                           self.subject,
                           message)
