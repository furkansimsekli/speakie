from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from random import shuffle

from . import forms
from .constants import TRANSLATION_PRACTICE_COEFFICIENT, SPEAKING_PRACTICE_COEFFICIENT
from .models import Course, TranslationPractice, SpeakingPractice, TranslationPracticeSolved


class CourseListView(View):
    def get(self, request):
        ctx = {
            'courses': Course.objects.filter(is_active=True)
        }
        return render(request, 'courses/course_list.html', ctx)

    def post(self, request):
        pass


class CourseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.CourseCreateForm()
        return render(request, 'courses/course_create.html', {'form': form})

    def post(self, request):
        title = request.POST.get('title')
        course = Course.objects.filter(title=title).first()
        form = forms.CourseCreateForm(request.POST, request.FILES, instance=course)

        if course and course.is_active:
            messages.warning(request, f'{title} course already exists!')
            return redirect('course-list')
        elif course and not course.is_active and form.is_valid():
            course.is_active = True
            form.save()
            messages.success(request, f'{title} course has been activated!')
            return redirect('course-list')

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully created a course!')
            return redirect('course-list')
        else:
            return render(request, 'courses/course_create.html', {'form': form})


class CourseUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        ctx = {
            'form': forms.CourseCreateForm(instance=course),
            'course_slug': course_slug
        }
        return render(request, 'courses/course_update.html', context=ctx)

    def post(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        form = forms.CourseCreateForm(request.POST, files=request.FILES, instance=course)

        ctx = {
            'form': forms.CourseCreateForm(instance=course),
            'course_slug': course_slug
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated!')
            return redirect('course-list')
        else:
            return render(request, 'courses/course_update.html', context=ctx)


class CourseDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        course.is_active = False
        course.save()
        messages.success(request, 'Successfully deleted the course!')
        return redirect('course-list')


class PracticeCategoryView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp_count = len(course.translationpractice_set.all())
        sp_count = len(course.speakingpractice_set.all())

        ctx = {
            'course': course,
            'tp_count': tp_count,
            'sp_count': sp_count
        }

        return render(request, 'courses/practice_category.html', ctx)

    def post(self, request, course_slug):
        pass


class TranslationPracticeListView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        translation_practices = course.translationpractice_set.all()
        tp_list = []

        for tp in translation_practices:
            is_solved = TranslationPracticeSolved.objects.filter(user=request.user, practice=tp).first()
            tp_list.append({'tp': tp, 'is_solved': is_solved})

        ctx = {
            'course_slug': course_slug,
            'tp_list': tp_list
        }

        return render(request, 'courses/translation_practice_list.html', ctx)

    def post(self, request, course_slug):
        pass


class TranslationPracticeCreateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        form = forms.TranslationPracticeCreateForm()

        ctx = {
            'course_slug': course_slug,
            'form': form
        }

        return render(request, 'courses/translation_practice_create.html', ctx)

    def post(self, request, course_slug):
        form = forms.TranslationPracticeCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New translation practice has been added to inventory!')
        else:
            messages.warning(request, 'The form you have sent is not valid!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp_list = course.translationpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'tp_list': tp_list
        }

        return render(request, 'courses/translation_practice_list.html', ctx)


class TranslationPracticeUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        tp = TranslationPractice.objects.filter(slug=tp_slug).first()
        form = forms.TranslationPracticeCreateForm(instance=tp)

        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'form': form
        }

        return render(request, 'courses/translation_practice_update.html', ctx)

    def post(self, request, course_slug, tp_slug):
        tp = TranslationPractice.objects.filter(slug=tp_slug).first()
        form = forms.TranslationPracticeCreateForm(request.POST, instance=tp)

        if form.is_valid():
            form.save()
            messages.success(request, 'Practice has been updated!')
        else:
            messages.warning(request, 'The form you have sent is not valid!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp_list = course.translationpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'tp_list': tp_list
        }

        return render(request, 'courses/translation_practice_list.html', ctx)


class TranslationPracticeDeleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        pass

    def post(self, request, course_slug, tp_slug):
        tp = TranslationPractice.objects.filter(slug=tp_slug).first()

        if tp:
            tp.delete()
            messages.success(request, 'Practice has been deleted!')
        else:
            messages.warning(request, 'Chosen practice does not exist!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp_list = course.translationpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'tp_list': tp_list
        }

        return render(request, 'courses/translation_practice_list.html', ctx)


class TranslationPracticeView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        tp = TranslationPractice.objects.filter(slug=tp_slug).first()
        shuffled_choices = [tp.answer, tp.choice_1, tp.choice_2, tp.choice_3]
        shuffle(shuffled_choices)
        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'tp': tp,
            'choices': shuffled_choices
        }

        return render(request, 'courses/translation_practice.html', ctx)

    def post(self, request, course_slug, tp_slug):
        tp = TranslationPractice.objects.filter(slug=tp_slug).first()
        user = request.user

        if request.POST.get('answer') == tp.answer:
            tp_solved = TranslationPracticeSolved.objects.filter(user=user, practice=tp)

            if tp_solved:
                messages.warning(request, 'You already solved this practice!')
            else:
                TranslationPracticeSolved.objects.create(user=user, practice=tp)
                points = tp.difficulty * TRANSLATION_PRACTICE_COEFFICIENT
                user.score += points
                user.save()
                messages.success(request, f'CORRECT! You have earned {points} points')
        else:
            messages.warning(request, f'WRONG! Correct answer: {tp.answer}')

        shuffled_choices = [tp.answer, tp.choice_1, tp.choice_2, tp.choice_3]
        shuffle(shuffled_choices)
        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'tp': tp,
            'choices': shuffled_choices
        }

        return render(request, 'courses/translation_practice.html', ctx)


class SpeakingPracticeListView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        sp_list = course.speakingpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'sp_list': sp_list
        }

        return render(request, 'courses/speaking_practice_list.html', ctx)

    def post(self, request, course_slug):
        pass


class SpeakingPracticeCreateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        form = forms.SpeakingPracticeCreateForm()

        ctx = {
            'course_slug': course_slug,
            'form': form
        }

        return render(request, 'courses/speaking_practice_create.html', ctx)

    def post(self, request, course_slug):
        form = forms.SpeakingPracticeCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'New speaking practice has been added to inventory!')
        else:
            messages.warning(request, 'The form you have sent is not valid!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        sp_list = course.speakingpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'sp_list': sp_list
        }

        return render(request, 'courses/speaking_practice_list.html', ctx)


class SpeakingPracticeUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        sp = SpeakingPractice.objects.filter(slug=sp_slug).first()
        form = forms.SpeakingPracticeCreateForm(instance=sp)

        ctx = {
            'course_slug': course_slug,
            'sp_slug': sp_slug,
            'form': form
        }

        return render(request, 'courses/speaking_practice_update.html', ctx)

    def post(self, request, course_slug, sp_slug):
        sp = SpeakingPractice.objects.filter(slug=sp_slug).first()
        form = forms.SpeakingPracticeCreateForm(request.POST, instance=sp)

        if form.is_valid():
            form.save()
            messages.success(request, 'Practice has been updated!')
        else:
            messages.warning(request, 'The form you have sent is not valid!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        sp_list = course.speakingpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'sp_list': sp_list
        }

        return render(request, 'courses/speaking_practice_list.html', ctx)


class SpeakingPracticeDeleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        pass

    def post(self, request, course_slug, sp_slug):
        sp = SpeakingPractice.objects.filter(slug=sp_slug).first()

        if sp:
            sp.delete()
            messages.success(request, 'Practice has been deleted!')
        else:
            messages.warning(request, 'Chosen practice does not exist!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        sp_list = course.speakingpractice_set.all()

        ctx = {
            'course_slug': course_slug,
            'sp_list': sp_list
        }

        return render(request, 'courses/speaking_practice_list.html', ctx)


class SpeakingPracticeView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        sp = SpeakingPractice.objects.filter(slug=sp_slug).first()

        ctx = {
            'course_slug': course_slug,
            'sp_slug': sp_slug,
            'sp': sp
        }

        return render(request, 'courses/speaking_practice.html', ctx)

    def post(self, request, course_slug, sp_slug):
        # TODO: Implement scoring mechanism
        pass
