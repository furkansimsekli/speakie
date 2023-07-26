from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.CourseListView.as_view(),
         name='course-list'),
    path('new/',
         views.CourseCreateView.as_view(),
         name='course-create'),
    path('<course_slug>/update/',
         views.CourseUpdateView.as_view(),
         name='course-update'),
    path('<course_slug>/delete/',
         views.CourseDeleteView.as_view(),
         name='course-delete'),
    path('<course_slug>/',
         views.PracticeCategoryView.as_view(),
         name='practice-category'),
    path('<course_slug>/translation-practice/',
         views.TranslationPracticeListView.as_view(),
         name='tp-list'),
    path('<course_slug>/translation-practice/new',
         views.TranslationPracticeCreateView.as_view(),
         name='tp-create'),
    path('<course_slug>/translation-practice/<tp_slug>/update/',
         views.TranslationPracticeUpdateView.as_view(),
         name='tp-update'),
    path('<course_slug>/translation-practice/<tp_slug>/delete/',
         views.TranslationPracticeDeleteView.as_view(),
         name='tp-delete'),
    path('<course_slug>/translation-practice/<tp_slug>/',
         views.TranslationPracticeView.as_view(),
         name='tp'),
    path('<course_slug>/speaking-practice/',
         views.SpeakingPracticeListView.as_view(),
         name='sp-list'),
    path('<course_slug>/speaking-practice/new',
         views.SpeakingPracticeCreateView.as_view(),
         name='sp-create'),
    path('<course_slug>/speaking-practice/<sp_slug>/update/',
         views.SpeakingPracticeUpdateView.as_view(),
         name='sp-update'),
    path('<course_slug>/speaking-practice/<sp_slug>/delete/',
         views.SpeakingPracticeDeleteView.as_view(),
         name='sp-delete'),
    path('<course_slug>/speaking-practice/<sp_slug>/',
         views.SpeakingPracticeView.as_view(),
         name='sp'),
    path('<course_slug>/translation-practice/<tp_slug>/api/',
         views.TranslationPracticeQuestionView.as_view(),
         name='tp-question'),
    path('<course_slug>/speaking-practice/<sp_slug>/api/',
         views.SpeakingPracticeQuestionView.as_view(),
         name='sp-question')
]
