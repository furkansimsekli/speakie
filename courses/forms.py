from django import forms

from .models import Course, TranslationPractice, SpeakingPractice

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'flag_picture']


class TranslationPracticeCreateForm(forms.ModelForm):
    class Meta:
        model = TranslationPractice
        fields = ['course', 'title', 'question', 'answer', 'difficulty']


class SpeakingPracticeCreateForm(forms.ModelForm):
    class Meta:
        model = SpeakingPractice
        fields = ['course', 'title', 'paragraph', 'difficulty']
