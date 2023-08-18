from django.shortcuts import render
from django.http import JsonResponse
from dictionary.models import Word, Synonym, Example
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dictionary.models import Word, Synonym, Example
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Create your views here.
def main(request):
    return render(request, 'transmeme/translator.html')
        
def translate(request):
    word1 = Word.objects.all() # 데이터베이스 가져오기
    wordinput = request.POST.get(str('content')) # 입력한 정보 가져오기 
    
    matching_words = []  # 유사한 단어들을 저장할 리스트
    
    for w in word1: # 모든 데이터에 접근할 수 있도록 반복문 
        similarity = fuzz.partial_ratio(wordinput, w.subject)  # 입력한 단어와 데이터베이스 단어의 유사도 계산
        if similarity >= 50:  # 유사도가 70 이상인 경우를 선택 (임의로 설정)
            matching_words.append((w, similarity))  # 유사한 단어를 리스트에 추가
    
    if matching_words:  # 유사한 단어가 하나 이상 있는 경우
        matching_words.sort(key=lambda x: x[1], reverse=True)  # 유사도에 따라 내림차순 정렬
        best_match = matching_words[0][0]  # 가장 유사한 단어 선택
        synonym = Synonym.objects.filter(word=best_match) 
        example = Example.objects.filter(word=best_match)  # 유사한 단어에 대한 정보 가져오기
        n = int(best_match.count)
        Word.objects.filter(subject=best_match).update(count=n + 1)  # 검색 1회 증가시킴
        lookup = Word.objects.all().order_by('-count')[:10]  # 검색횟수에 따른 딕셔너리 추가(순서정렬 후 앞에서부터 10개)
        context = {
            "word": best_match,
            "wordinput": wordinput,
            'syno': synonym[0],
            'ex': example[0],
            "count": lookup
        }  # context에 넣어서 HTML로 전달
        return render(request, 'transmeme/result.html', context)
    
    # 유사한 단어가 없는 경우
    lookup = Word.objects.all().order_by('-count')[:10]  # 검색횟수에 따른 딕셔너리 추가(순서정렬 후 앞에서부터 10개)
    context = {
        "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
        "wordinput": wordinput,
        'syno': "해당 없음",
        'ex': '해당 없음',
        "count": lookup
    }
    return render(request, 'transmeme/result.html', context)

@api_view(['POST'])
def translate_api(request):
    data = request.data
    wordinput = data.get('content')
    
    word_match = Word.objects.filter(subject=wordinput).first()
    if not word_match:
        # 유사한 단어 처리를 위한 코드
        matching_words = []
        for w in Word.objects.all():
            similarity = fuzz.partial_ratio(wordinput, w.subject)
            if similarity >= 50:
                matching_words.append((w, similarity))
        
        if matching_words:
            matching_words.sort(key=lambda x: x[1], reverse=True)
            word_match = matching_words[0][0]
        else:
            lookup = Word.objects.all().order_by('-count')[:10]
            context = {
                "word": {
                    "subject": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
                    "meaning": "",
                    "standard": "다시 입력해 주세요",
                    "count": 0,
                },
                "wordinput": wordinput,
                'syno': "해당 없음",
                'ex': '해당 없음',
                "count": WordSerializer(lookup, many=True).data,
            }
            return Response(context)
    
    synonym = Synonym.objects.filter(word=word_match).first()
    example = Example.objects.filter(word=word_match).first()

    n = int(word_match.count)
    word_match.count = n + 1
    word_match.save()

    lookup = Word.objects.all().order_by('-count')[:10]
    
    context = {
        "word": WordSerializer(word_match).data,
        "wordinput": wordinput,
        "syno": SynonymSerializer(synonym).data if synonym else "해당 없음",
        "ex": ExampleSerializer(example).data if example else "해당 없음",
        "count": WordSerializer(lookup, many=True).data,
    }
    return Response(context)

    
    synonym = Synonym.objects.filter(word=word_match).first()
    example = Example.objects.filter(word=word_match).first()

    n = int(word_match.count)
    word_match.count = n + 1
    word_match.save()

    lookup = Word.objects.all().order_by('-count')[:10]
    
    context = {
        "word": WordSerializer(word_match).data,
        "wordinput": wordinput,
        "syno": SynonymSerializer(synonym).data if synonym else "해당 없음",
        "ex": ExampleSerializer(example).data if example else "해당 없음",
        "count": WordSerializer(lookup, many=True).data,
    }
    # print(context)
    return Response(context)


# def translate(request):
#     word1 = Word.objects.all() #데이터베이스 가져오기
#     wordinput = request.POST.get(str('content')) #입력한 정보 가져오기 
#     for w in word1: # 모든 데이터에 접근할 수 있도록 반복문 
#         if wordinput == w.subject: #입력한 정보와 접근된 제이터와 같다면
#             synonym = Synonym.objects.filter(word=w) 
#             example = Example.objects.filter(word=w) #유의어와 예문 가져오기
#             n = int(w.count)
#             Word.objects.filter(subject=w).update(count = n + 1) # 검색 1회 증가시킴
#             lookup=Word.objects.all().order_by('-count')[:10] # 검색횟수에 따른 딕셔너리 추가(순서정렬 후 앞에서부터 10개)
#             context = {
#                 "word": w,
#                 "wordinput": wordinput,
#                 'syno': synonym[0],
#                 'ex': example[0],
#                 "count": lookup
#             } #context에 잘 넣어서 html로 쏴줌 
#             return render(request, 'transmeme/result.html', context)

#     # If no matching word is found, return this context 
#     lookup=Word.objects.all().order_by('-count')[:10] #없을 경우에 대해서 동작 설명
#     context = {
#         "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#         "wordinput": wordinput,
#         'syno': "해당 없음",
#         'ex': '해당 없음',
#         "count": lookup
#     }
#     return render(request, 'transmeme/result.html', context)


# @api_view(['POST'])
# def translate_api(request):
#     data = request.data
#     wordinput = data.get('content')
#     print(wordinput)
#     word_match = Word.objects.filter(subject=wordinput).first()
#     print(word_match)
#     if word_match:
#         synonym = Synonym.objects.filter(word=word_match).first()
#         example = Example.objects.filter(word=word_match).first()

#         n = int(word_match.count)
#         word_match.count = n + 1
#         word_match.save()

#         lookup = Word.objects.all().order_by('-count')[:10]
        
#         context = {
#             "word": WordSerializer(word_match).data,
#             "wordinput": wordinput,
#             "syno": SynonymSerializer(synonym).data if synonym else "해당 없음",
#             "ex": ExampleSerializer(example).data if example else "해당 없음",
#             "count": WordSerializer(lookup, many=True).data,
#         }
#         print(context)
#         return Response(context)

#     lookup = Word.objects.all().order_by('-count')[:10]
#     context = {
#         "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#         "wordinput": wordinput,
#         'syno': "해당 없음",
#         'ex': '해당 없음',
#         "count": WordSerializer(lookup, many=True).data,
#     }
#     print(context)
#     return Response(context)
