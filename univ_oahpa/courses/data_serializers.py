from rest_framework import serializers

from .models import Goal, GoalParameter, UserFeedbackLog, UserGoalInstance

__all__ = [
    'GoalParamSerializer',
    'GoalSerializer',
    'FeedbackLogSerializer',
    'StatusSerializer',
]

class GoalParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalParameter
        fields = ('parameter', 'value')

# TODO: edit/put
class GoalSerializer(serializers.ModelSerializer):
    begin_url = serializers.CharField(source='begin_url', read_only=True)
    params = GoalParamSerializer(many=True)
    # TODO: validate that name and desc aren't empty

    def transform_params(self, obj, value):
        """ Need to switch all these to dictionaries
        """
        if value is not None:
            return dict([(p.get('parameter'), p.get('value')) for p in value])
        return None

    class Meta:
        model = Goal
        fields = ('id', 'short_name', 'description', 'begin_url',
                  'course', 'params', 'main_type', 'sub_type',
                  'threshold', 'minimum_sets_attempted',
                  'correct_first_try')

class FeedbackLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedbackLog
        fields = ('feedback_texts', 'user_input', 'correct_answer', 'datetime')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGoalInstance
        fields = ('progress', 'rounds', 'total_answered', 'correct', 'completed_date', 'grade', 'correct_first_try', 'is_complete')

