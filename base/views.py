from django.db.models import F, IntegerField
from django.db.models.functions import Log, Ceil
from django.shortcuts import render
from django.views import View

from courses.models import Course, TranslationPractice, SpeakingPractice
from users.models import User


class HomeView(View):
    def get(self, request):
        course_count = Course.objects.filter(is_active=True).count()
        tp_count = TranslationPractice.objects.all().count()
        sp_count = SpeakingPractice.objects.all().count()
        leaderboard = User.objects.annotate(
            level=Ceil(Log(1.5, F('score') * 0.005 + 1), output_field=IntegerField())).order_by('-score', 'id')
        ctx = {
            'course_count': course_count,
            'tp_count': tp_count,
            'sp_count': sp_count,
            'leaderboard': leaderboard,
            'title': 'Home'
        }
        return render(request, 'base/home.html', ctx)

    def post(self, request):
        pass


class AboutView(View):
    def get(self, request):
        return render(request, 'base/about.html', {'title': 'About'})

    def post(self, request):
        pass
