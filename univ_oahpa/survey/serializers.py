from rest_framework import serializers

from .models import ( Survey
                    , UserSurvey
                    , UserSurveyQuestionAnswer
                    , SurveyQuestion
                    , SurveyQuestionAnswerValue
                    )

__all__ = [
    'QASerializer',
    'SurveyQuestionSerializer',
    'SurveySerializer',
    'UserSurveySerializer',
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

class UserQASerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSurveyQuestionAnswer
        fields = ('question', 'answer_text', )


class UserSurveySerializer(serializers.ModelSerializer):

    user_answers = UserQASerializer(many=True, required=False)
    user_anon = serializers.CharField(source='user_anonymized',
                                      read_only=True)

    class Meta:
        model = UserSurvey
        fields = ('survey', 'user_anon', 'completed', 'user_answers', )
