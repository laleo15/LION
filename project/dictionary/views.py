from django.shortcuts import render, get_object_or_404
from .models import Word,Synonym,Example
# Create your views here.

# def list(request):
#      word_list = Word.objects.order_by('subject')
#      context = {'word_list': word_list}
#      return render(request, 'dictionary/search.html', context)\
     
     
def calculate_initial_sound(character):
    base_code = ord('가')
    code = ord(character) - base_code
    initial_sound_index = code // 28 // 21
    initial_sound = chr(initial_sound_index + 0x1100)
    return initial_sound

def categorize_words_by_initial_sound(words):
    categorized_words = {}
    for word in words:
        initial_sound = calculate_initial_sound(word.subject[0])
        if initial_sound not in categorized_words:
            categorized_words[initial_sound] = []
        categorized_words[initial_sound].append(word)
    return categorized_words

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
     word = Word.objects.get(id=word_id)
     syno= Synonym.objects.get(id=word_id)
     ex = Example.objects.get(id=word_id)
     context = {'word': word,'syno':syno,'ex':ex}
     return render(request, 'dictionary/word_detail.html', context)

