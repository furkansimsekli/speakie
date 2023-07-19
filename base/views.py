from django.shortcuts import render
from django.views import View

from courses.models import Course, TranslationPractice, SpeakingPractice
from users.models import User


class HomeView(View):
    def get(self, request):
        course_count = Course.objects.filter(is_active=True).count()
        tp_count = TranslationPractice.objects.all().count()
        sp_count = SpeakingPractice.objects.all().count()
        leaderboard = User.objects.all().order_by('-score')
        ctx = {
            'course_count': course_count,
            'tp_count': tp_count,
            'sp_count': sp_count,
            'leaderboard': leaderboard
        }
        return render(request, 'base/home.html', ctx)

    def post(self, request):
        pass


class AboutView(View):
    def get(self, request):
        return render(request, 'base/about.html')

    def post(self, request):
        pass
