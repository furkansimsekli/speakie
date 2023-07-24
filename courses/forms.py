from django import forms

from .models import Course, TranslationPractice, SpeakingPractice


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'flag_picture']

    def clean_title(self):
        return self.cleaned_data['title'].title()


class TranslationPracticeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True

    class Meta:
        model = TranslationPractice
        fields = ['course', 'title', 'question', 'answer', 'choice_1', 'choice_2', 'choice_3', 'difficulty']

    def clean_title(self):
        return self.cleaned_data['title'].title()


class SpeakingPracticeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True

    class Meta:
        model = SpeakingPractice
        fields = ['course', 'title', 'paragraph', 'difficulty']

    def clean_title(self):
        return self.cleaned_data['title'].title()
