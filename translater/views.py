from rest_framework import generics
from .models import TeacherGroup, Lesson, Word, Test, TestQuestion
from .serializers import (
    TeacherGroupSerializer,
    LessonSerializer,
    WordSerializer,
    TestSerializer,
    TestQuestionSerializer,
)


class TeacherGroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer


class TeacherGroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class WordListCreateAPIView(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class TestListCreateAPIView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer


class TestQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer
