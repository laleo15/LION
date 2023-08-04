from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TestQuestion

class QuestionAdmin(admin.ModelAdmin):
    search_fields=['subject']

admin.site.register(TestQuestion, QuestionAdmin)
