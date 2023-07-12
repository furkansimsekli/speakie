from django import forms
from .models import Course


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'flag']
