from django.shortcuts import render
from dictionary.models import Word, Synonym, Example
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer


# Create your views here.
def main(request):
    return render(request, 'transmeme/translator.html')
        
def translate(request):
    word1 = Word.objects.all()
    wordinput = request.POST.get(str('content'))
    for w in word1:
        if wordinput == w.subject:
            synonym = Synonym.objects.filter(word=w)
            example = Example.objects.filter(word=w)
            n = int(w.count)
            Word.objects.filter(subject=w).update(count = n + 1)
            lookup=Word.objects.all().order_by('-count')[:10]
            context = {
                "word": w,
                "wordinput": wordinput,
                'syno': synonym[0],
                'ex': example[0],
                "count": lookup
            }
            return render(request, 'transmeme/result.html', context)

    # If no matching word is found, return this context
    lookup=Word.objects.all().order_by('-count')[:10]
    context = {
        "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
        "wordinput": wordinput,
        'syno': "해당 없음",
        'ex': '해당 없음',
        "count": lookup
    }
    return render(request, 'transmeme/result.html', context)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer

@api_view(['GET'])
def get_word_detail(request, word_text):
    word = Word.objects.get(subject=word_text)
    word_serializer = WordSerializer(word)
    
    synonym = Synonym.objects.filter(word=word)
    synonym_serializer = SynonymSerializer(synonym[0])
    
    example = Example.objects.filter(word=word)
    example_serializer = ExampleSerializer(example[0])
    
    data = {
        'word': word_serializer.data,
        'synonym': synonym_serializer.data,
        'example': example_serializer.data
    }
    
    return Response(data)
