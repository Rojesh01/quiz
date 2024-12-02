from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)


class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question , QuestionAdmin)
admin.site.register(Answer)

