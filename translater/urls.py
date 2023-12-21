from django.urls import path, include
from rest_framework import routers
from .views import (
    TeacherGroupListCreateAPIView,
    TeacherGroupDetailAPIView,
    LessonListCreateAPIView,
    LessonDetailAPIView,
    WordListCreateAPIView,
    WordDetailAPIView,
    # TestListCreateAPIView,
    # TestDetailAPIView,
    TestViewSet,
    TestQuestionListCreateAPIView,
    TestQuestionDetailAPIView,
)

router = routers.DefaultRouter()
router.register(r"test", TestViewSet)

urlpatterns = [
    path('teacher-groups/', TeacherGroupListCreateAPIView.as_view(), name='teacher_group_list_create'),
    path('teacher-groups/<int:pk>/', TeacherGroupDetailAPIView.as_view(), name='teacher_group_detail'),

    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson_list_create'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),

    path('words/', WordListCreateAPIView.as_view(), name='word_list_create'),
    path('words/<int:pk>/', WordDetailAPIView.as_view(), name='word_detail'),
    path('set/', include(router.urls)),
    # path('tests/', TestListCreateAPIView.as_view(), name='test_list_create'),
    # path('tests/<int:pk>/', TestDetailAPIView.as_view(), name='test_detail'),
    # path('words/<int:pk>/', TestViewSet.as_view(), name='word_detail'),

    path('test-questions/', TestQuestionListCreateAPIView.as_view(), name='test_question_list_create'),
    path('test-questions/<int:pk>/', TestQuestionDetailAPIView.as_view(), name='test_question_detail'),
]

