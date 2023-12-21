from django.contrib import admin
from .models import TeacherGroup, TestQuestion, Test, Lesson, Word

admin.site.register(TeacherGroup)
admin.site.register(Lesson)
admin.site.register(Word)
admin.site.register(Test)
admin.site.register(TestQuestion)