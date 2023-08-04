from django.shortcuts import render, get_object_or_404
from .models import Word,Synonym,Example
# Create your views here.

def list(request):
     word_list = Word.objects.order_by('subject')
     context = {'word_list': word_list}
     return render(request, 'dictionary/search.html', context)

def detail(request, word_id):
     word = Word.objects.get(id=word_id)
     syno= Synonym.objects.get(id=word_id)
     ex = Example.objects.get(id=word_id)
     context = {'word': word,'syno':syno,'ex':ex}
     return render(request, 'dictionary/word_detail.html', context)