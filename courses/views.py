from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from . import forms
from .models import Course, TranslationPractice, SpeakingPractice


class CourseListView(View):
    def get(self, request):
        ctx = {
            'courses': Course.objects.filter(is_active=True)
        }
        return render(request, 'courses/course_list.html', ctx)

    def post(self, request):
        pass


class CourseCreateView(View):
    def get(self, request):
        form = forms.CourseCreateForm()
        return render(request, 'courses/course_create.html', {'form': form})

    def post(self, request):
        if request.user.is_moderator:
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
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')


class CourseUpdateView(View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        ctx = {
            'form': forms.CourseCreateForm(instance=course),
            'course_slug': course_slug
        }
        return render(request, 'courses/course_update.html', context=ctx)

    def post(self, request, course_slug):
        if request.user.is_moderator:
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
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')


class CourseDeleteView(View):
    def get(self, request):
        pass

    def post(self, request, course_slug):
        if request.user.is_moderator:
            course = Course.objects.filter(is_active=True, slug=course_slug).first()
            course.is_active = False
            course.save()
            messages.success(request, 'Successfully deleted the course!')
            return redirect('course-list')
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')


class PracticeListView(View):
    def get(self, request, course_slug):
        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp = course.translationpractice_set.all()
        sp = course.speakingpractice_set.all()

        ctx = {
            'tp': tp,
            'sp': sp,
            'course_slug': course_slug
        }
        return render(request, 'courses/practice_list.html', context=ctx)

    def post(self, request):
        pass


class PracticeCreateView(View):
    def get(self, request, course_slug):
        if request.user.is_moderator:
            tp_form = forms.TranslationPracticeCreateForm()
            sp_form = forms.SpeakingPracticeCreateForm()
            ctx = {
                'tp_form': tp_form,
                'sp_form': sp_form,
                'course_slug': course_slug
            }
            return render(request, 'courses/practice_create.html', context=ctx)
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')

    def post(self, request, course_slug):
        if request.user.is_moderator:
            tp_form = forms.TranslationPracticeCreateForm(request.POST)
            sp_form = forms.SpeakingPracticeCreateForm(request.POST)
            course = Course.objects.filter(is_active=True, slug=course_slug).first()
            tp = course.translationpractice_set.all()
            sp = course.speakingpractice_set.all()

            ctx = {
                'tp': tp,
                'sp': sp,
                'course_slug': course_slug
            }

            if tp_form.is_valid():
                tp_form.save()
                messages.success(request, 'New translation practice has been published!')
                return render(request, 'courses/practice_list.html', context=ctx)
            elif sp_form.is_valid():
                sp_form.save()
                messages.success(request, 'New speaking practice has been published!')
                return render(request, 'courses/practice_list.html', context=ctx)
            else:
                ctx = {
                    'tp_form': tp_form,
                    'sp_form': sp_form,
                    'course_slug': course_slug
                }
                return render(request, 'courses/practice_create.html', context=ctx)
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')


class PracticeUpdateView(View):
    def get(self, request, course_slug, practice_slug):
        if request.user.is_moderator:
            tp = TranslationPractice.objects.filter(slug=practice_slug).first()

            if tp:
                form = forms.TranslationPracticeCreateForm(instance=tp)
            else:
                sp = SpeakingPractice.objects.filter(slug=practice_slug).first()
                form = forms.SpeakingPracticeCreateForm(instance=sp)

            ctx = {
                'form': form,
                'course_slug': course_slug,
                'practice_slug': practice_slug,
            }
            return render(request, 'courses/practice_update.html', context=ctx)
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')

    def post(self, request, course_slug, practice_slug):
        if request.user.is_moderator:
            tp = TranslationPractice.objects.filter(slug=practice_slug).first()

            if tp:
                tp_form = forms.TranslationPracticeCreateForm(request.POST, instance=tp)
                if tp_form.is_valid():
                    tp_form.save()
                    messages.success(request, 'Translation practice has been successfully updated!')
            else:
                sp = SpeakingPractice.objects.filter(slug=practice_slug).first()
                sp_form = forms.SpeakingPracticeCreateForm(request.POST, instance=sp)
                if sp_form.is_valid():
                    sp_form.save()
                    messages.success(request, 'Speaking practice has been successfully updated!')

            course = Course.objects.filter(is_active=True, slug=course_slug).first()
            tp = course.translationpractice_set.all()
            sp = course.speakingpractice_set.all()

            ctx = {
                'tp': tp,
                'sp': sp,
                'course_slug': course_slug
            }
            return render(request, 'courses/practice_list.html', context=ctx)
        else:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')


class PracticeDeleteView(View):
    def get(self, request):
        pass

    def post(self, request, course_slug, practice_slug):
        tp = TranslationPractice.objects.filter(slug=practice_slug).first()

        if tp:
            tp.delete()
            messages.success(request, 'Translation practice has been successfully deleted!')
        else:
            sp = SpeakingPractice.objects.filter(slug=practice_slug).first()
            if sp:
                sp.delete()
                messages.success(request, 'Translation practice has been successfully deleted!')

        course = Course.objects.filter(is_active=True, slug=course_slug).first()
        tp = course.translationpractice_set.all()
        sp = course.speakingpractice_set.all()

        ctx = {
            'tp': tp,
            'sp': sp,
            'course_slug': course_slug
        }
        return render(request, 'courses/practice_list.html', context=ctx)


class PracticeView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        pass
