from django.shortcuts import render, get_object_or_404
from .models import Word, Synonym, Example
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WordWithInitialSoundSerializer, WordSerializer, SynonymSerializer, ExampleSerializer

# def calculate_initial_sound(character):
#     base_code = ord('가')
#     code = ord(character) - base_code
#     initial_sound_index = code // 28 // 21
#     initial_sound = chr(initial_sound_index + 0x1100)
#     return initial_sound

def calculate_initial_sound(character):
    if '가' <= character <= '힣':
        base_code = ord('가')
        code = ord(character) - base_code
        initial_sound_index = code // 28 // 21
        initial_sound = chr(initial_sound_index + 0x1100)
    else:
        initial_sound = '#'
    return initial_sound

def categorize_words_by_initial_sound(words):
    categorized_words = {}
    for word in words:
        initial_sound = calculate_initial_sound(word.subject[0])
        if initial_sound not in categorized_words:
            categorized_words[initial_sound] = []
        categorized_words[initial_sound].append(word)
    return categorized_words

@api_view(["GET"])
def WordListAPI(request):
    word_queryset = Word.objects.all()
    synonym_queryset = Synonym.objects.all()
    example_queryset = Example.objects.all()

    word_serializer = WordWithInitialSoundSerializer(word_queryset, many=True)
    synonym_serializer = SynonymSerializer(synonym_queryset, many=True)
    example_serializer = ExampleSerializer(example_queryset, many=True)

    data = {
        'words': word_serializer.data,
        'synonyms': synonym_serializer.data,
        'examples': example_serializer.data,
    }

    return Response(data)

def list(request):
    word_list = Word.objects.order_by('subject')
    categorized_word_list = categorize_words_by_initial_sound(word_list)
    context = {'categorized_word_list': categorized_word_list}
    return render(request, 'dictionary/search_all.html', context)

def list1(request):
    word_list = Word.objects.order_by('generation', 'subject')
    categorized_by_generation = {}

    for word in word_list:
        generation = word.generation
        if generation not in categorized_by_generation:
            categorized_by_generation[generation] = []
        categorized_by_generation[generation].append(word)

    categorized_word_list = {}
    for generation, words in categorized_by_generation.items():
        categorized_word_list[generation] = categorize_words_by_initial_sound(words)

    context = {'categorized_word_list': categorized_word_list}
    return render(request, 'dictionary/search_generation.html', context)

def detail(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    syno = Synonym.objects.filter(word=word)
    ex = Example.objects.filter(word=word)
    context = {'word': word, 'syno': syno, 'ex': ex}
    return render(request, 'dictionary/word_detail.html', context)


@api_view(['GET'])
def detail_serialized(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    syno = Synonym.objects.filter(word=word)
    ex = Example.objects.filter(word=word)

    word_serializer = WordSerializer(word)
    syno_serializer = SynonymSerializer(syno, many=True) if syno else None
    ex_serializer = ExampleSerializer(ex, many=True) if ex else None

    serialized_data = {
        "word": word_serializer.data,
        "syno": syno_serializer.data if syno_serializer else [],
        "ex": ex_serializer.data if ex_serializer else [],
    }
    return Response(serialized_data)
