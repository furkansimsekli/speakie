from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('new/', views.CourseCreateView.as_view(), name='course-create'),
    path('<course_slug>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<course_slug>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('<course_slug>/', views.PracticeListView.as_view(), name='practice-list'),
    path('<course_slug>/new/', views.PracticeCreateView.as_view(), name='practice-create'),
    path('<course_slug>/<practice_slug>/update/', views.PracticeUpdateView.as_view(), name='practice-update'),
    path('<course_slug>/<practice_slug>/delete/', views.PracticeDeleteView.as_view(), name='practice-delete'),
    path('<course_slug>/<practice_slug>/', views.PracticeView.as_view(), name='practice'),
]
