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
from .serializers import WordSerializer, SynonymSerializer, ExampleSerializer,InputSerializer


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

# @csrf_exempt
# @api_view(['POST'])
# def translate1(request):
#     if request.method == 'POST':
#         wordinput = request.POST.get('content')
#         try:
#             word = Word.objects.get(subject=wordinput)
#             synonym = Synonym.objects.filter(word=word)
#             example = Example.objects.filter(word=word)
#             n = int(word.count)
#             word.count = n + 1
#             word.save()

#             word_serializer = WordSerializer(word)
#             synonym_serializer = SynonymSerializer(synonym[0]) if synonym else None
#             example_serializer = ExampleSerializer(example[0]) if example else None

#             context = {
#                 "word": word_serializer.data,
#                 "syno": synonym_serializer.data if synonym_serializer else "해당 없음",
#                 "ex": example_serializer.data if example_serializer else "해당 없음",
#             }
#             return render(request, 'transmeme/result.html', context)
#         except Word.DoesNotExist:
#             context = {
#                 "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#                 "syno": "해당 없음",
#                 "ex": "해당 없음",
#             }
#             return render(request, 'transmeme/result.html', context)

# @csrf_exempt
# @api_view(['POST'])
# def get_rank(request):
#     words = Word.objects.all().order_by('-count')[:10]
#     word_list = [{"subject": word.subject} for word in words]
#     return Response(word_list)



# @api_view(['GET'])
# def send_translate(request):
#     word1 = Word.objects.all() #데이터베이스 가져오기
#     wordinput = request.POST.get(str('content')) #입력한 정보 가져오기 
#     for w in word1: # 모든 데이터에 접근할 수 있도록 반복문 
#         if wordinput == w.subject: #입력한 정보와 접근된 제이터와 같다면
#             synonym = Synonym.objects.filter(word=w) 
#             example = Example.objects.filter(word=w) #유의어와 예문 가져오기
#             n = int(w.count)
#             Word.objects.filter(subject=w).update(count = n + 1) # 검색 1회 증가시킴
#             lookup=Word.objects.all().order_by('-count')[:10] # 검색횟수에 따른 딕셔너리 추가(순서정렬 후 앞에서부터 10개)
#             kk={}
#             for i in range(0,10):
#                 key = f'key_{i+1}'
#                 kk[key] =  lookup[i]
#             context = {
#                 "word": w,
#                 "wordinput": wordinput,
#                 'syno': synonym[0],
#                 'ex': example[0],
#                 "count": kk
#             } #context에 잘 넣어서 html로 쏴줌
#             json_data=json.dumps(context)
#             return render(request, 'transmeme/result.html', json_data)

#     # If no matching word is found, return this context 
#     lookup=Word.objects.all().order_by('-count')[:10] #없을 경우에 대해서 동작 설명
#     kk={}
#     for i in range(0,10):
#         key = f'key_{i+1}'
#         kk[key] =  lookup[i]
    
#     context = {
#         "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#         "wordinput": wordinput,
#         'syno': "해당 없음",
#         'ex': '해당 없음',
#         "count": kk
#     }
#     json_data=json.dumps(context)
#     return render(request, 'transmeme/result.html', json_data)

# @api_view(['POST'])
# def translate_api(request):
#     data = request.data
#     wordinput = data.get('content')
#     wordinput = request.POST.get(str('content'))

#     word_match = Word.objects.filter(subject=wordinput).first()

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

#         return render(request, 'transmeme/result.html', context)

#     lookup = Word.objects.all().order_by('-count')[:10]
#     context = {
#         "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#         "wordinput": wordinput,
#         'syno': "해당 없음",
#         'ex': '해당 없음',
#         "count": WordSerializer(lookup, many=True).data,
#     }

#     return render(request, 'transmeme/result.html', context)


# @api_view(['POST'])
# def translate_api(request):
#     word=Word.objects.all()
#     if request.method=="POST":
#         word_data=request.data()
#         word_input=InputSerializer(data=word_data)
#         pritn
#         for w in word:
#             if word_input==w.subject:
#                 synonym = Synonym.objects.filter(word=w) 
#                 example = Example.objects.filter(word=w) #유의어와 예문 가져오기
#                 n=int(w.count)
#                 Word.objects.filter(subject=w).update(count = n + 1) # 검색 1회 증가시킴
#                 lookup=Word.objects.all().order_by('-count')[:10]
                
#                 word_serializer = WordSerializer(word)
#                 synonym_serializer = SynonymSerializer(synonym)
#                 example_serializer = ExampleSerializer(example)
#                 lookup_serializer = WordSerializer(lookup)
                
#                 context = {
#                     "word": word_serializer,
#                     "wordinput": word_input,
#                     "syno": synonym_serializer,
#                     "ex": example_serializer,
#                     "count": lookup_serializer,
#                 }
#                 print(context)
#                 return render(request, 'transmeme/result.html', context)
            
#         lookup=Word.objects.all().order_by('-count')[:10]
#         lookup_serializer = WordSerializer(lookup , many = True )
#         context = {
#             "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
#             "wordinput": word_input,
#             'syno': "해당 없음",
#             'ex': '해당 없음',
#             "count": lookup_serializer,
#         }
#         return render(request, 'transmeme/result.html', context)

@api_view(['POST'])
def translate_api(request):
    data = request.data
    wordinput = data.get('content')
    print(wordinput)
    word_match = Word.objects.filter(subject=wordinput).first()
    print(word_match)
    if word_match:
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
        print(context)
        return Response(context)

    lookup = Word.objects.all().order_by('-count')[:10]
    context = {
        "word": "잘못 입력하셨거나, 등록되지 않은 정보입니다. 다시 입력해 주세요",
        "wordinput": wordinput,
        'syno': "해당 없음",
        'ex': '해당 없음',
        "count": WordSerializer(lookup, many=True).data,
    }
    print(context)
    return Response(context)
