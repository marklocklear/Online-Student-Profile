from django.conf import settings
from django.core.mail import EmailMessage

def email_user(from_user, to_user, bcc_user, subject, body):
    """Used to intercept emails when in debug mode"""
    subject = subject.rstrip('\n')
    if settings.DEBUG:
        if bcc_user:
            subject = '(Bcc: ' + bcc_user + ') ' + subject
        subject = '(Orig: ' + to_user + ') ' + subject
        for debug_user in settings.DEBUG_USERS:
            message = EmailMessage(subject, body, from_user, [debug_user[1]])
            message.content_subtype = 'html'
            message.send()
    else:
        if bcc_user:
            message = EmailMessage(subject,
                                   body,
                                   from_user,
                                   [to_user],
                                   [bcc_user])
        else:
            message = EmailMessage(subject,
                                   body,
                                   from_user,
                                   [to_user])
        message.content_subtype = 'html'
        message.send()
    return
