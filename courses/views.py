from random import shuffle

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from . import forms, utils
from .constants import TRANSLATION_PRACTICE_COEFFICIENT
from .models import (
    Course,
    TranslationPractice,
    SpeakingPractice,
    TranslationPracticeSolved,
    SpeakingPracticeSolved,
    AudioRecord
)


class CourseListView(View):
    def get(self, request):
        ctx = {
            'courses': Course.objects.filter(is_active=True).order_by('title', 'id'),
            'title': 'Courses'
        }
        return render(request, 'courses/course_list.html', ctx)

    def post(self, request):
        pass


class CourseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.CourseCreateForm()
        return render(request, 'courses/course_create.html', {'form': form, 'title': 'New Course'})

    def post(self, request):
        form = forms.CourseCreateForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            course = Course.objects.filter(title=title).first()

            if course and course.is_active:
                messages.warning(request, f'{title} course already exists!')
            elif course and not course.is_active:
                course.is_active = True
                form.save()
                messages.success(request, f'{title} course has been activated!')
            else:
                form.save()
                messages.success(request, 'Successfully created a course!')

            return redirect('course-list')
        else:
            messages.warning(request, 'The form you have sent is not valid!')

        return render(request, 'courses/course_create.html', {'form': form, 'title': 'New Course'})


class CourseUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        ctx = {
            'form': forms.CourseCreateForm(instance=course),
            'course_slug': course_slug,
            'title': 'Update Course'
        }
        return render(request, 'courses/course_update.html', context=ctx)

    def post(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        form = forms.CourseCreateForm(request.POST, files=request.FILES, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated!')
            return redirect('course-list')
        else:
            ctx = {
                'form': forms.CourseCreateForm(instance=course),
                'course_slug': course_slug,
                'title': 'Update Course'
            }
            messages.warning(request, 'The form you have sent is not valid!')
            return render(request, 'courses/course_update.html', context=ctx)


class CourseDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        course.is_active = False
        course.save()
        messages.success(request, 'Successfully deleted the course!')
        return redirect('course-list')


class PracticeCategoryView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        tp_count = len(course.translationpractice_set.all())
        sp_count = len(course.speakingpractice_set.all())
        ctx = {
            'course': course,
            'tp_count': tp_count,
            'sp_count': sp_count,
            'title': 'Categories'
        }
        return render(request, 'courses/practice_category.html', ctx)

    def post(self, request, course_slug):
        pass


class TranslationPracticeListView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        translation_practices = course.translationpractice_set.all().order_by('difficulty', 'id')
        tp_list = []

        for tp in translation_practices:
            is_solved = TranslationPracticeSolved.objects.filter(user=request.user, practice=tp).first()
            tp_list.append({'tp': tp, 'is_solved': is_solved})

        page = request.GET.get('page', 1)
        paginator = Paginator(tp_list, per_page=10)
        page_object = paginator.get_page(page)
        ctx = {
            'course_slug': course_slug,
            'page_obj': page_object,
            'title': 'TP List'
        }
        return render(request, 'courses/translation_practice_list.html', ctx)

    def post(self, request, course_slug):
        pass


class TranslationPracticeCreateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        form = forms.TranslationPracticeCreateForm(initial={'course': course})
        ctx = {
            'course_slug': course_slug,
            'form': form,
            'title': 'New TP'
        }
        return render(request, 'courses/translation_practice_create.html', ctx)

    def post(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        form = forms.TranslationPracticeCreateForm(request.POST, initial={'course': course})

        if form.is_valid():
            form.save()
            messages.success(request, 'New translation practice has been added to inventory!')
        else:
            ctx = {
                'course_slug': course_slug,
                'form': form,
                'title': 'New TP'
            }
            messages.warning(request, 'The form you have sent is not valid!')
            return render(request, 'courses/translation_practice_create.html', ctx)

        return redirect(reverse('tp-list', kwargs={'course_slug': course_slug}))


class TranslationPracticeUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        tp = get_object_or_404(TranslationPractice, slug=tp_slug)
        form = forms.TranslationPracticeCreateForm(instance=tp)
        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'form': form,
            'title': 'Update TP'
        }
        return render(request, 'courses/translation_practice_update.html', ctx)

    def post(self, request, course_slug, tp_slug):
        tp = get_object_or_404(TranslationPractice, slug=tp_slug)
        form = forms.TranslationPracticeCreateForm(request.POST, instance=tp)

        if form.is_valid():
            form.save()
            messages.success(request, 'Practice has been updated!')
        else:
            ctx = {
                'course_slug': course_slug,
                'tp_slug': tp_slug,
                'form': form,
                'title': 'Update TP'
            }
            messages.warning(request, 'The form you have sent is not valid!')
            return render(request, 'courses/translation_practice_update.html', ctx)

        return redirect(reverse('tp-list', kwargs={'course_slug': course_slug}))


class TranslationPracticeDeleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        pass

    def post(self, request, course_slug, tp_slug):
        tp = get_object_or_404(TranslationPractice, slug=tp_slug)

        if tp:
            tp.delete()
            messages.success(request, 'Practice has been deleted!')
        else:
            messages.warning(request, 'Chosen practice does not exist!')

        return redirect(reverse('tp-list', kwargs={'course_slug': course_slug}))


class TranslationPracticeView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'title': 'TP'
        }
        return render(request, 'courses/translation_practice.html', ctx)

    def post(self, request, course_slug, tp_slug):
        tp = get_object_or_404(TranslationPractice, slug=tp_slug)
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

        return redirect(reverse('tp', kwargs={'course_slug': course_slug, 'tp_slug': tp_slug}))

    @staticmethod
    def find_prev_and_next(tp):
        prev_tp = TranslationPractice.objects.filter(course=tp.course, difficulty__lte=tp.difficulty).filter(
            id__lt=tp.id).order_by('-difficulty', '-id').first()
        next_tp = TranslationPractice.objects.filter(course=tp.course, difficulty__gte=tp.difficulty).filter(
            id__gt=tp.id).order_by('difficulty', 'id').first()
        return prev_tp, next_tp


class SpeakingPracticeListView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        speaking_practices = course.speakingpractice_set.all().order_by('difficulty', 'id')
        sp_list = []

        for sp in speaking_practices:
            is_solved = SpeakingPracticeSolved.objects.filter(user=request.user, practice=sp).first()
            sp_list.append({'sp': sp, 'is_solved': is_solved})

        page = request.GET.get('page', 1)
        paginator = Paginator(sp_list, per_page=3)
        page_object = paginator.get_page(page)
        ctx = {
            'course_slug': course_slug,
            'page_obj': page_object,
            'title': 'SP List'
        }
        return render(request, 'courses/speaking_practice_list.html', ctx)

    def post(self, request, course_slug):
        pass


class SpeakingPracticeCreateView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        form = forms.SpeakingPracticeCreateForm(initial={'course': course})
        ctx = {
            'course_slug': course_slug,
            'form': form,
            'title': 'New SP'
        }
        return render(request, 'courses/speaking_practice_create.html', ctx)

    def post(self, request, course_slug):
        course = get_object_or_404(Course, is_active=True, slug=course_slug)
        form = forms.SpeakingPracticeCreateForm(request.POST, initial={'course': course})

        if form.is_valid():
            form.save()
            messages.success(request, 'New speaking practice has been added to inventory!')
        else:
            ctx = {
                'course_slug': course_slug,
                'form': form,
                'title': 'New SP'
            }
            messages.warning(request, 'The form you have sent is not valid!')
            return render(request, 'courses/speaking_practice_create.html', ctx)

        return redirect(reverse('sp-list', kwargs={'course_slug': course_slug}))


class SpeakingPracticeUpdateView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        sp = get_object_or_404(SpeakingPractice, slug=sp_slug)
        form = forms.SpeakingPracticeCreateForm(instance=sp)
        ctx = {
            'course_slug': course_slug,
            'sp_slug': sp_slug,
            'form': form,
            'title': 'Update SP'
        }
        return render(request, 'courses/speaking_practice_update.html', ctx)

    def post(self, request, course_slug, sp_slug):
        sp = get_object_or_404(SpeakingPractice, slug=sp_slug)
        form = forms.SpeakingPracticeCreateForm(request.POST, instance=sp)

        if form.is_valid():
            form.save()
            messages.success(request, 'Practice has been updated!')
        else:
            ctx = {
                'course_slug': course_slug,
                'sp_slug': sp_slug,
                'form': form,
                'title': 'Update SP'
            }
            messages.warning(request, 'The form you have sent is not valid!')
            return render(request, 'courses/speaking_practice_update.html', ctx)

        return redirect(reverse('sp-list', kwargs={'course_slug': course_slug}))


class SpeakingPracticeDeleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        pass

    def post(self, request, course_slug, sp_slug):
        sp = get_object_or_404(SpeakingPractice, slug=sp_slug)

        if sp:
            sp.delete()
            messages.success(request, 'Practice has been deleted!')
        else:
            messages.warning(request, 'Chosen practice does not exist!')

        return redirect(reverse('sp-list', kwargs={'course_slug': course_slug}))


class SpeakingPracticeView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        ctx = {
            'course_slug': course_slug,
            'sp_slug': sp_slug,
            'title': 'SP'
        }
        return render(request, 'courses/speaking_practice.html', ctx)

    def post(self, request, course_slug, sp_slug):
        audio_file = utils.save_audio_file(request.body)
        sp = get_object_or_404(SpeakingPractice, slug=sp_slug)
        record = AudioRecord.objects.create(audio_file=audio_file, user=request.user, practice=sp)
        transcript = utils.speech_to_text(record.audio_file.path, sp.course.language_code)
        print("Transcript:", transcript)
        return HttpResponse()

    @staticmethod
    def find_prev_and_next(sp):
        prev_tp = SpeakingPractice.objects.filter(course=sp.course, difficulty__lte=sp.difficulty).filter(
            id__lt=sp.id).order_by('-difficulty', '-id').first()
        next_tp = SpeakingPractice.objects.filter(course=sp.course, difficulty__gte=sp.difficulty).filter(
            id__gt=sp.id).order_by('difficulty', 'id').first()
        return prev_tp, next_tp


class TranslationPracticeQuestionView(LoginRequiredMixin, View):
    def get(self, request, course_slug, tp_slug):
        tp = get_object_or_404(TranslationPractice, slug=tp_slug)
        shuffled_choices = [tp.answer, tp.choice_1, tp.choice_2, tp.choice_3]
        shuffle(shuffled_choices)
        prev_tp, next_tp = TranslationPracticeView.find_prev_and_next(tp)
        is_solved = TranslationPracticeSolved.objects.filter(user=request.user, practice=tp).first()
        ctx = {
            'course_slug': course_slug,
            'tp_slug': tp_slug,
            'tp': tp,
            'choices': shuffled_choices,
            'prev_tp': prev_tp,
            'next_tp': next_tp,
            'is_solved': is_solved,
            'title': 'TP'
        }
        html_content = render(request, 'courses/translation_practice_question.html', ctx)
        return HttpResponse(html_content)


class SpeakingPracticeQuestionView(LoginRequiredMixin, View):
    def get(self, request, course_slug, sp_slug):
        sp = get_object_or_404(SpeakingPractice, slug=sp_slug)
        prev_sp, next_sp = SpeakingPracticeView.find_prev_and_next(sp)
        is_solved = SpeakingPracticeSolved.objects.filter(user=request.user, practice=sp).first()
        ctx = {
            'course_slug': course_slug,
            'sp_slug': sp_slug,
            'sp': sp,
            'prev_sp': prev_sp,
            'next_sp': next_sp,
            'is_solved': is_solved,
            'title': 'SP'
        }
        html_content = render(request, 'courses/speaking_practice_question.html', ctx)
        return HttpResponse(html_content)
