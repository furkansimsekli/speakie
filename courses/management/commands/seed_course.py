import json

from django.core.management.base import BaseCommand

from courses.models import Course, SpeakingPractice


class Command(BaseCommand):
    help = 'Populates the speaking practice tables'

    def handle(self, *args, **options):
        with open('sp_data.json', 'r') as f:
            courses = json.load(f)
            self.stdout.write('Course JSON loaded...')

        for course in courses:
            self.stdout.write(f'Current: {course["title"]}')
            Course.objects.create(title=course['title'], description=course['description'],
                                  language_code=course['language_code'])

        with open('sp_data.json', 'r') as f:
            practices = json.load(f)
            self.stdout.write('Speaking Practice JSON loaded...')

        for practice in practices:
            self.stdout.write(f'Current: {practice["title"]}')
            course = Course.objects.filter(title=practice['course']).first()
            SpeakingPractice.objects.create(course=course, title=practice['title'], paragraph=practice['paragraph'],
                                            difficulty=practice['difficulty'])
