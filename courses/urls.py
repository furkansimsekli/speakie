from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='home'),
    path('<course_id>/', views.PracticeListView.as_view(), name='practice-list'),
    path('<course_id>/<practice_id>/', views.PracticeView.as_view(), name='practice')
]
