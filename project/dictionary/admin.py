from django.contrib import admin
from .models import Word, Synonym, Example


class WordAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Word, WordAdmin)
admin.site.register(Synonym)
admin.site.register(Example)