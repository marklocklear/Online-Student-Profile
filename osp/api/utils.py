from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from osp.core.models import UserProfile

def validate_credentials(request, authorized_hosts, valid_key, provided_key):
    if not provided_key:
        raise Exception('Missing authorization key')

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        host_received = request.META['HTTP_X_FORWARDED_FOR']
    elif request.META.has_key('REMOTE_ADDR'):
        host_received = request.META['REMOTE_ADDR']
    else:
        raise Exception("Missing host IP address")

    if host_received.strip() in authorized_hosts:
        if valid_key != provided_key:
            raise Exception("Invalid authorization key")
    else:
        raise Exception("Unauthorized host IP address")

    return

def load_users(data, groups):
    # Store references to user groups
    g = Group.objects.filter(name__in=groups)

    # Let's keep a count of how many new and updated objects we have
    # Also, how many user accounts we activate or deactivate
    users_updated = 0
    users_created = 0

    # Grab all existing users and their associated objects in the
    # specified groups from the database
    all_users = UserProfile.objects.filter(
        user__groups__name__in=groups
    ).distinct().select_related()

    # Find or create user objects for each user
    for u in data:
        # Check if the user has a user account
        if u['username']:
            username = u['username']
        # If the user does not have a user account, assign them a
        # temporary username based on their ID number
        else:
            if 'Students' in groups:
                username = '%ss' % u['id_number']
            elif 'Employees' in groups:
                username = '%se' % u['id_number']

        # Get the existing user object or create a new one
        new_user = False
        try:
            user = all_users.filter(id_number=u['id_number'])[0].user
        except IndexError:
            try:
                user = User.objects.create_user(username, u['email'], u['last_four'])
                new_user = True
            except IntegrityError, (errno, strerror):
                # If the user record already exists and just isn't in
                # the correct group (and therefore not in the queryset
                # we pulled earlier), grab it
                # MySQL error # 1062 = duplicate entry
                if errno == 1062:
                    user = User.objects.get(username=username)

        # Increment counter for appropriate operation type
        # Get or create the user profile object associated with the user
        if new_user:
            profile = UserProfile.objects.create(user=user)
            users_created += 1
        else:
            try:
                profile = all_users.filter(user=user)[0]
            except IndexError:
                try:
                    profile = UserProfile.objects.create(user=user)
                except IntegrityError, (errno, strerror):
                    if errno == 1062:
                        profile = UserProfile.objects.get(user=user)
            users_updated += 1

        # Check if anything changed before updating the user object
        if (user.username != username
            or user.first_name != u['first_name']
            or user.last_name != u['last_name']
            or user.email != u['email']
            or user.is_active != u['is_active']):
            user.username = username
            user.first_name = u['first_name']
            user.last_name = u['last_name']
            user.email = u['email']
            user.is_active = u['is_active']

            user.save()
        elif new_user:
            user.save()

        # Make sure that user is in the appropriate groups
        [user.groups.add(group)
         for group in g
         if group not in user.groups.all()]

        # Check if anything changed before updating the profile object
        if (profile.id_number != u['id_number']
            or profile.phone_number != u['phone_number']):
            profile.id_number = u['id_number']
            profile.phone_number = u['phone_number']

            profile.save()

    # Return statistics on user account creation and modification
    return (len(data), users_updated, users_created)
