from django.shortcuts import render
from django.views import View


class CourseListView(View):
    def get(self, request):
        return render(request, 'courses/home.html')
