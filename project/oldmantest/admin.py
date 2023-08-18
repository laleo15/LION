from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TestQuestion,Comment

class QuestionAdmin(admin.ModelAdmin):
    search_fields=['subject']

admin.site.register(TestQuestion, QuestionAdmin)
#admin.site.register(User, UserAdmin)
admin.site.register(Comment)