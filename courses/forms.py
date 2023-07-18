from django import forms

from .models import Course, TranslationPractice, SpeakingPractice

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'flag_picture']


class TranslationPracticeCreateForm(forms.ModelForm):
    class Meta:
        model = TranslationPractice
        fields = ['course', 'title', 'question', 'answer', 'choice_1', 'choice_2', 'choice_3', 'difficulty']


class SpeakingPracticeCreateForm(forms.ModelForm):
    class Meta:
        model = SpeakingPractice
        fields = ['course', 'title', 'paragraph', 'difficulty']