from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, TranslationPractice
from .forms import NewCourseForm


class CourseListView(View):
    def get(self, request):
        context = {
            'courses': Course.objects.all()
        }
        return render(request, 'courses/home.html', context)


class CourseCreateView(View):
    def get(self, request):
        if request.user.profile.moderator:
            form = NewCourseForm()
            return render(request, 'courses/course_create.html', {'form': form})

        return redirect('home')

    def post(self, request):
        if request.user.profile.moderator:
            form = NewCourseForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                messages.success(request, f'Successfully created a new course!')

        return redirect('home')


class CourseDeleteView(View):
    def get(self, request, course_id):
        if request.user.profile.moderator:
            Course.objects.filter(id=course_id).delete()
        else:
            messages.warning(request, 'You are not authorized to this!')

        return redirect('home')


class PracticeListView(View):
    def get(self, request, course_id):
        context = {
            'translation_practices': TranslationPractice.objects.filter(course=course_id)
        }
        return render(request, 'courses/practice_list.html', context)


class PracticeView(LoginRequiredMixin, View):
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
