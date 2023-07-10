from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .models import Course, TranslationPractice


class CourseListView(View):
    def get(self, request):
        context = {
            'courses': Course.objects.all()
        }
        return render(request, 'courses/home.html', context)


class PracticeListView(View):
    def get(self, request, course_id):
        context = {
            'translation_practices': TranslationPractice.objects.filter(course=course_id)
        }
        return render(request, 'courses/practice_list.html', context)


class PracticeView(View):
    def get(self, request, course_id, practice_id):
        practice = TranslationPractice.objects.filter(id=practice_id).first()
        context = {
            'practice': practice
        }
        return render(request, 'courses/translation_practice.html', context)

    def post(self, request, course_id, practice_id):
        practice = TranslationPractice.objects.filter(id=practice_id).first()

        context = {
            'practice': practice
        }

        if request.POST.get('answer') == practice.answer:
            messages.success(request, "That's correct! You got X points!")
        else:
            messages.warning(request, "Nope, that's not the correct answer! Think harder...")

        return render(request, 'courses/translation_practice.html', context)
