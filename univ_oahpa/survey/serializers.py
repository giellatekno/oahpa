from rest_framework import serializers

from .models import ( Survey
                    , UserSurvey
                    , SurveyQuestion
                    , SurveyQuestionAnswerValue
                    )

__all__ = [
    'QASerializer',
    'SurveyQuestionSerializer',
    'SurveySerializer',
]

class QASerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyQuestionAnswerValue
        fields = ('answer_text', )

class SurveyQuestionSerializer(serializers.ModelSerializer):

    answer_values = serializers.RelatedField(many=True, required=False)

    class Meta:
        model = SurveyQuestion
        fields = ('id', 'question_text', 'question_type', 'answer_values', )

class SurveySerializer(serializers.ModelSerializer):

    questions = SurveyQuestionSerializer()

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'questions', )
