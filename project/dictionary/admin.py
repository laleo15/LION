from django.contrib import admin
from .models import Word, Meaning


class WordAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Word, WordAdmin)
admin.site.register(Meaning)