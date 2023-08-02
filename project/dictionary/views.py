from django.shortcuts import render, get_object_or_404
from .models import Word
# Create your views here.

def list(request):
     word_list = Word.objects.order_by('subject')
     context = {'word_list': word_list}
     return render(request, 'dictionary/search.html', context)

def detail(request, word_id):
     word = get_object_or_404(Word, pk=word_id)
     word = Word.objects.get(id=word_id)
     context = {'word': word}
     return render(request, 'dictionary/word_detail.html', context)

# def mean(request, word_id):
#      word = get_object_or_404(Meaning, pk=word_id)
#      word = Word.objects.get(id=word_id)
#      context = {'word': word}
#      return render(request, 'dictionary/word_detail.html', context)