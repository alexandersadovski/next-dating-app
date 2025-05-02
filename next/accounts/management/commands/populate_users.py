import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from next.accounts.models import Profile


class Command(BaseCommand):
    help = 'Populate the database with mock users and profiles.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of mock users to create (default: 50)',
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        user_model = get_user_model()

        if count < 2:
            self.stdout.write(self.style.ERROR('Please provide a count greater than 1.'))
            return

        # Determine the number of males and females
        num_males = count // 2
        num_females = count - num_males

        genders = ['Male'] * num_males + ['Female'] * num_females
        random.shuffle(genders)

        created_users = 0

        with transaction.atomic():
            for gender in genders:
                try:
                    email = fake.unique.email()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error generating unique email: {e}'))
                    continue

                password = 'password123'  # Default password

                # Create AppUser
                user = user_model.objects.create_user(
                    email=email,
                    password=password,
                    is_active=True,
                )

                # Create Profile
                first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
                last_name = fake.last_name()
                age = random.randint(18, 60)
                location = fake.city()
                bio = fake.text(max_nb_chars=200)
                profile_picture = None

                Profile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    gender=gender,
                    location=location,
                    bio=bio,
                    profile_picture=profile_picture,
                )

                created_users += 1
                self.stdout.write(self.style.SUCCESS(f'Created user {email} with profile.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_users} users and profiles.'))
