from rest_framework import serializers
from .models import TeacherGroup, Lesson, Word, Test, TestQuestion, TestResult


class TeacherGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherGroup
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        depth = 1


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'original_word']

class TestResultSerializer(serializers.ModelSerializer):
    test = TestSerializer()

    class Meta:
        model = TestResult
        fields = ['user', 'test', 'mark']