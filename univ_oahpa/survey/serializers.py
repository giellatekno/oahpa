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

    answers = QASerializer(source='question_answer', many=True, required=False)

    class Meta:
        model = SurveyQuestion
        fields = ('question_text', 'question_type', 'answers', )

class SurveySerializer(serializers.ModelSerializer):

    questions = SurveyQuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = ('title', 'description', 'questions', )


###     def transform_params(self, obj, value):
###         """ Need to switch all these to dictionaries
###         """
###         if value is not None:
###             return dict([(p.get('parameter'), p.get('value')) for p in value])
###         return None
