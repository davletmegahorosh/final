from django.db import models


class TeacherGroup(models.Model):
    name = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    topic = models.CharField(max_length=255)
    date = models.DateField()
    status = models.BooleanField(default=False)
    teacher_group = models.ForeignKey('TeacherGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class Word(models.Model):
    original_word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_word


class Test(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TestQuestion(models.Model):
    original_word = models.CharField(max_length=255)
    user_translation = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_word