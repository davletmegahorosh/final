from rest_framework import serializers
from .models import TeacherGroup, Lesson, Word, Test, TestQuestion


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


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = '__all__'
