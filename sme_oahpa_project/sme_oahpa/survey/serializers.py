from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

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
        fields = ('id', 'question_text', 'question_type', 'answer_values', )

class SurveySerializer(serializers.ModelSerializer):

    questions = SurveyQuestionSerializer()

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'questions', )

class UserQASerializer(serializers.ModelSerializer):

    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserSurveyQuestionAnswer
        fields = ('question', 'answer_text', )

class UserSurveySerializer(serializers.ModelSerializer):

    user_answers = UserQASerializer(many=True, required=False)
    user_anon = serializers.CharField(source='user_anonymized',
                                      read_only=True, required=False)
    description = serializers.DateTimeField(required=False)

    class Meta:
        model = UserSurvey
        fields = ('survey', 'user_anon', 'completed', 'user_answers', )

    def validate(self, attrs):
        """ Return a validation error to handle the unique_together
        constraint, of one user submission per survey, but do this after
        the main validation of everything else.
        """

        attrs = super(UserSurveySerializer, self).validate(attrs)

        # Return a failure if a survey exists for the values already.
        survey = attrs.get('survey')
        user = self.context.get('request').user
        exists = self.Meta.model.objects.filter(user_id=user.id,
                                                survey_id=survey.id).exists()
        if exists:
            raise serializers.ValidationError(_("You have already submitted this survey once."))

        return attrs
