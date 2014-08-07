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
        fields = ('answer_text', 'id', )

class SurveyQuestionSerializer(serializers.ModelSerializer):

    answer_values = QASerializer(many=True, required=False)

    class Meta:
        model = SurveyQuestion
        fields = ('id', 'question_text', 'question_type', 'answer_values', 'required', )

class SurveySerializer(serializers.ModelSerializer):

    questions = SurveyQuestionSerializer()

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'questions', )
