from django.contrib import admin
from .models import WordQuiz

class QuizAdmin(admin.ModelAdmin):
    search_fields=['subject']
    
admin.site.register(WordQuiz, QuizAdmin)