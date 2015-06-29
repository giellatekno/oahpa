from rest_framework import serializers

from sms_drill.models import ( Word
                             , Form
                             , Tag
                             , Semtype
                             )

__all__ = [
    'WordSerializer',
    'FormSerializer',
    'TagSerializer',
]

class SemtypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Semtype
        fields = ('semtype', )
        depth = 1


class WordSerializer(serializers.ModelSerializer):

    lemma = serializers.CharField(blank=True, required=False)
    pos = serializers.CharField(required=False)
    stem = serializers.CharField(required=False)
    wordclass = serializers.CharField(required=False)
    semtype = SemtypeSerializer(many=True)

    class Meta:
        model = Word
        depth = 1
        fields = ('lemma', 'pos', 'stem', 'wordclass', 'semtype', )

class TagSerializer(serializers.ModelSerializer):

    string = serializers.CharField(blank=True, required=False)

    class Meta:
        model = Tag
        fields = ('string', 'pos', )

class FormSerializer(serializers.ModelSerializer):

    fullform = serializers.CharField(blank=True, required=False)
    tag = TagSerializer(blank=True, required=False)
    word = WordSerializer(blank=True, required=False)

    class Meta:
        model = Form
        fields = ('fullform', 'tag', 'word', )

