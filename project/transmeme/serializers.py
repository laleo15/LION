from rest_framework import serializers
from dictionary.models import Word, Synonym, Example

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
