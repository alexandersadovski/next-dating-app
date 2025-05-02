import getpass
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a new report reviewer staff user (non-superuser)'

    def handle(self, *args, **kwargs):
        user_model = get_user_model()

        # Prompt for email
        email = None
        while email is None:
            email = input('Email: ').strip()
            if not email:
                self.stderr.write('Error: Email cannot be blank.')
                email = None
            elif user_model.objects.filter(email=email).exists():
                self.stderr.write('Error: That email is already taken.')
                email = None

        # Prompt for password
        password = None
        while password is None:
            password = getpass.getpass()
            password2 = getpass.getpass('Password (again): ')
            if password != password2:
                self.stderr.write("Error: Your passwords didn't match.")
                password = None
            else:
                try:
                    validate_password(password)
                except exceptions.ValidationError as err:
                    self.stderr.write('\n'.join(err.messages))
                    password = None

        # Create the user
        user = user_model.objects.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = False
        user.save()

        # Assign the user to the 'Report Reviewers' group
        reviewer_group, created = Group.objects.get_or_create(name='Report Reviewers')

        # Assign permissions to the group
        self.assign_permissions_to_group(reviewer_group)

        user.groups.add(reviewer_group)

        self.stdout.write(self.style.SUCCESS(
            f'Report Reviewer "{email}" created successfully and added to "Report Reviewers" group.'
        ))

    def assign_permissions_to_group(self, group):
        # Define the permissions you want to assign to the Report Reviewers group
        permissions_codenames = [
            ('reports', 'report', 'view_report'),
            ('reports', 'report', 'change_report'),
            ('accounts', 'profile', 'view_profile'),
            ('messaging', 'message', 'view_message'),
        ]

        permissions = []

        for app_label, model_name, codename in permissions_codenames:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                permission = Permission.objects.get(content_type=content_type, codename=codename)
                permissions.append(permission)
            except ContentType.DoesNotExist:
                self.stderr.write(f'Error: ContentType for {app_label}.{model_name} does not exist.')
            except Permission.DoesNotExist:
                self.stderr.write(f'Error: Permission {codename} for {app_label}.{model_name} does not exist.')

        # Assign permissions to the group
        group.permissions.set(permissions)
