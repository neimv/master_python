from dataclasses import fields
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    fields = ("choice_text", )
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ("pub_date", "question_text",)
    inlines = (ChoiceInline, )
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date", )
    search_fields = ("question_text",)

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)