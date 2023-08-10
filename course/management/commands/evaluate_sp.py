from django.core.management.base import BaseCommand
from django.urls import reverse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from course import utils
from course.constants import SPEAKING_PRACTICE_COEFFICIENT
from course.models import SpeakingPracticeEvaluation, SpeakingPracticeSolution
from notification.models import Notification


class Command(BaseCommand):
    help = 'Evaluates speaking practice submissions that exists in the queue'

    def handle(self, *args, **options):
        self.stdout.write('Executing evaluate_sp...')
        submissions = SpeakingPracticeEvaluation.objects.filter(is_done=False)

        for submission in submissions:
            self.stdout.write(f'Now: {submission.id}')
            user = submission.audio_record.owner
            practice = submission.audio_record.practice
            sp_solved = SpeakingPracticeSolution.objects.filter(user=user, practice=practice).first()
            transcript = utils.speech_to_text(audio_file=submission.audio_record.audio_file.path,
                                              language=practice.course.language_code)
            accuracy = utils.calculate_accuracy(original=practice.paragraph, transcript=transcript)
            score = int(SPEAKING_PRACTICE_COEFFICIENT * practice.difficulty * accuracy)

            if not sp_solved:
                sp_solved = SpeakingPracticeSolution.objects.create(user=user, practice=practice)

            if score > sp_solved.point:
                if accuracy >= 0.80:
                    sp_solved.is_successful = True

                user.score += score - sp_solved.point
                sp_solved.point = score
                sp_solved.transcript = transcript

            # TODO: move into another function
            message = f'Horayyy! You gained {score} points from "{practice.title}" practice!'
            course_slug = practice.course.slug
            sp_slug = practice.slug
            url = reverse('sp', kwargs={'course_slug': course_slug, 'sp_slug': sp_slug})
            Notification.objects.create(owner=user, message=message, url=url)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{user.id}',
                {
                    'type': 'notify_user',
                    'message': message,
                    'url': url
                }
            )

            submission.is_completed = True
            sp_solved.save()
            user.save()
            submission.save()
            self.stdout.write(f'Done!')
