from django.core.management.base import BaseCommand

from courses import utils
from courses.constants import SPEAKING_PRACTICE_COEFFICIENT
from courses.models import SpeakingPracticeEvaluation, SpeakingPracticeSolved


class Command(BaseCommand):
    help = 'Evaluates speaking practice submissions that exists in the queue'

    def handle(self, *args, **options):
        self.stdout.write('Executing evaluate_sp...')
        submissions = SpeakingPracticeEvaluation.objects.filter(is_done=False)

        for submission in submissions:
            self.stdout.write(f'Now: {submission.id}')
            user = submission.audio_record.owner
            practice = submission.audio_record.practice
            sp_solved = SpeakingPracticeSolved.objects.filter(user=user, practice=practice).first()
            transcript = utils.speech_to_text(audio_file=submission.audio_record.audio_file.path,
                                              language=practice.course.language_code)
            accuracy = utils.calculate_accuracy(original=practice.paragraph, transcript=transcript)
            score = int(SPEAKING_PRACTICE_COEFFICIENT * practice.difficulty * accuracy)

            if not sp_solved:
                sp_solved = SpeakingPracticeSolved.objects.create(user=user, practice=practice)

            if score > sp_solved.point:
                if accuracy >= 0.80:
                    sp_solved.is_completed = True

                user.score += score - sp_solved.point
                sp_solved.point = score
                sp_solved.save()
                user.save()

            submission.is_done = True
            submission.save()
            self.stdout.write(f'Done!')
