from django.contrib import admin
from .models import TestQuestion, Userdata

class QuestionAdmin(admin.ModelAdmin):
    search_fields=['subject']

admin.site.register(TestQuestion, QuestionAdmin)
admin.site.register(Userdata)