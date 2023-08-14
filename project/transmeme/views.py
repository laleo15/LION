from django.shortcuts import render
from django.http import JsonResponse
from dictionary.models import Word, Synonym, Example
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response



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


def main(request):
    return render(request, 'transmeme/transmeme.html')

@csrf_exempt
@api_view(['POST'])
def translate(request):
    if request.method == 'POST':
        wordinput = request.POST.get('content')
        try:
            word = Word.objects.get(subject=wordinput)
            synonym = Synonym.objects.filter(word=word)
            example = Example.objects.filter(word=word)
            n = int(word.count)
            word.count = n + 1
            word.save()

            word_serializer = WordSerializer(word)
            synonym_serializer = SynonymSerializer(synonym[0]) if synonym else None
            example_serializer = ExampleSerializer(example[0]) if example else None

            context = {
                "word": word_serializer.data,
                "syno": synonym_serializer.data if synonym_serializer else "해당 없음",
                "ex": example_serializer.data if example_serializer else "해당 없음",
            }
            return render(request, 'transmeme/result.html', context)
        except Word.DoesNotExist:
            context = {
                "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
                "syno": "해당 없음",
                "ex": "해당 없음",
            }
            return render(request, 'transmeme/result.html', context)

@csrf_exempt
@api_view(['GET'])
def get_rank(request):
    words = Word.objects.all().order_by('-count')[:10]
    word_list = [{"subject": word.subject} for word in words]
    return Response(word_list)
