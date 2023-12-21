from rest_framework import generics, viewsets, permissions, views
from rest_framework.response import Response

from .models import TeacherGroup, Lesson, Word, Test, TestQuestion, TestResult
from .serializers import (
    TeacherGroupSerializer,
    LessonSerializer,
    WordSerializer,
    TestSerializer,
    TestQuestionSerializer,
    QuestionSerializer
)


class TeacherGroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer


class TeacherGroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializers_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            lesson = Lesson.objects.get(id=pk)
            words = Word.objects.filter(lesson__id=pk)
            test = Test.objects.get(lesson__id=pk)
            test_serializer = TestSerializer(test)
            lesson_serializer = LessonSerializer(lesson)
            word_serializer = WordSerializer(words)
            return Response({'lesson': lesson_serializer.data,
                             'words': word_serializer.data,
                             'test': test_serializer.data})
        else:
            return Response({'error': 'No pk provided'})

class TestDuration(views.ApiView):
    def get(self, pk):
        test = Test.objects.get(id=pk)
        questions = Word.objects.filter(id = pk)
        test_serializer = TestSerializer(test)
        question_serializer = QuestionSerializer(questions)
        return Response({"test" : test_serializer,
                         "questions" : question_serializer})
    def post(self, request, pk):
        answers = request.data
        c = 0
        point = 100/len(answers.keys)
        for question, ans in answers:
            tq = Word.objects.get(id=question)
            word_serializer = WordSerializer(tq)
            if word_serializer.translation == ans:
                c+=1
        TestResult.objects.create(
            user = request.user,
            lesson = pk,
            mark = point*c
        )
        return Response({"your results : " : c*point})



# class LessonListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer

#
# class WordListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Word.objects.all()
#     serializer_class = WordSerializer
#
#
# class WordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Word.objects.all()
#     serializer_class = WordSerializer


# class TestListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer
#
#
# class TestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer

class TestViewSet(viewsets.ModelViewSet):
    serializers_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            test =TestQuestion.objects.filter(test__id=pk)
            serializer = TestSerializer(test)
            return Response({'test': serializer.data})
        else:
            return Response({'error': 'No pk provided'})


class TestQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer


class TestQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer

