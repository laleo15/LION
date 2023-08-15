from rest_framework import serializers
from .models import Word, Synonym, Example

def calculate_initial_sound(character):
    base_code = ord('가')
    code = ord(character) - base_code
    initial_sound_index = code // 28 // 21
    initial_sound = chr(initial_sound_index + 0x1100)
    return initial_sound

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = '__all__'

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'

class WordWithInitialSoundSerializer(serializers.ModelSerializer):
    initial_sound = serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = '__all__'
        read_only_fields = ('initial_sound',)

    def get_initial_sound(self, obj):
        return calculate_initial_sound(obj.subject[0])
