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
    word1 = Word.objects.all() #데이터베이스 가져오기
    wordinput = request.POST.get(str('content')) #입력한 정보 가져오기 
    for w in word1: # 모든 데이터에 접근할 수 있도록 반복문 
        if wordinput == w.subject: #입력한 정보와 접근된 제이터와 같다면
            synonym = Synonym.objects.filter(word=w) 
            example = Example.objects.filter(word=w) #유의어와 예문 가져오기
            n = int(w.count)
            Word.objects.filter(subject=w).update(count = n + 1) # 검색 1회 증가시킴
            lookup=Word.objects.all().order_by('-count')[:10] # 검색횟수에 따른 딕셔너리 추가(순서정렬 후 앞에서부터 10개)
            context = {
                "word": w,
                "wordinput": wordinput,
                'syno': synonym[0],
                'ex': example[0],
                "count": lookup
            } #context에 잘 넣어서 html로 쏴줌 
            return render(request, 'transmeme/result.html', context)

    # If no matching word is found, return this context 
    lookup=Word.objects.all().order_by('-count')[:10] #없을 경우에 대해서 동작 설명
    context = {
        "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
        "wordinput": wordinput,
        'syno': "해당 없음",
        'ex': '해당 없음',
        "count": lookup
    }
    return render(request, 'transmeme/result.html', context)

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
