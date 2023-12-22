from rest_framework import generics, viewsets, permissions, views
from rest_framework.response import Response

from .models import TeacherGroup, Lesson, Word, Test, TestQuestion, TestResult
from .serializers import (
    TeacherGroupSerializer,
    LessonSerializer,
    WordSerializer,
    TestSerializer,
    TestQuestionSerializer,
    QuestionSerializer, TestResultSerializer,

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

class TestDuration(views.APIView):
    def get(self, request, pk):
        test = Test.objects.get(id=pk)
        words = Word.objects.filter(lesson=test.lesson)
        test_serializer = TestSerializer(test)
        question_serializer = QuestionSerializer(words, many=True)

        return Response({"test": test_serializer.data, "questions": question_serializer.data})

    def post(self, request, pk):
        answers = request.data
        c = 0
        point = 100 / len(answers)

        test = Test.objects.get(id=pk)

        existing_result = TestResult.objects.filter(user=request.user, test=test)
        if existing_result.exists():
            return Response({"error": "You have already taken this test."}, status=400)

        for question_id, user_answer in answers.items():
            try:
                tq = Word.objects.get(id=question_id)
            except Word.DoesNotExist:
                return Response({"error": f"Word with ID {question_id} does not exist."}, status=400)

            word_serializer = WordSerializer(tq)

            if word_serializer.data['translation'] == user_answer:
                c += 1

        TestResult.objects.create(
            user=request.user,
            test=test,
            mark=point * c
        )

        return Response({"your results: ": c * point})



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
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            test_questions = TestQuestion.objects.filter(test__id=pk)
            serializer = TestQuestionSerializer(test_questions, many=True)
            return Response({'test_questions': serializer.data})
        else:
            return Response({'error': 'No pk provided'})



class TestQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer


class TestQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer

