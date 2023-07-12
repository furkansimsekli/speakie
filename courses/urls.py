from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='home'),
    path('new/', views.CourseCreateView.as_view(), name='course-create'),
    path('<course_id>/', views.PracticeListView.as_view(), name='practice-list'),
    path('<course_id>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<course_id>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('<course_id>/<practice_id>/', views.PracticeView.as_view(), name='practice')
]
