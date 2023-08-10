import sys

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = 'Creates a moderator with given credentials'

    def handle(self, *args, **options):
        username = input('Username: ')
        user = User.objects.filter(username=username).first()

        if user:
            self.stdout.write('ERROR: Username is already in use!')
            sys.exit(1)

        email = input('Email: ')
        user = User.objects.filter(email=email).first()

        if user:
            self.stdout.write('ERROR: Email is already in use!')
            sys.exit(1)

        password = input('Password: ')

        if len(password) == 0:
            self.stdout.write('ERROR: Please choose a password longer than 1 character!')
            sys.exit(1)

        password = make_password(password)
        User.objects.create(username=username, email=email, password=password, is_moderator=True)
        self.stdout.write('Done!')
