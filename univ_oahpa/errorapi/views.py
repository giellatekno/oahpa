from django.conf import settings

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .processes import XFST
from .log import ERROR_FST_LOG

ERROR_FST_SETTINGS = settings.ERROR_FST_SETTINGS

class FeedbackMessageStore(object):

    def get_message(self, iso, error_tag):
        """
            >>> messagestore.get_message("sme", "CGErr")
            "You forgot consonant gradation!"
        """
        # TODO:

        return message

    def parse(self):
        """ Reads the XML file and stores all messages """
        # TODO:

        return

    def __init__(self, xml_path):
        self.path = xml_path
        self.parse()
        # TODO:

class FeedbackFST(objects):

	def get_all_feedback_for_form(self, input_wordform):
		# TODO:
		return self.lookup_proc.lookup([input_wordform])

	def get_constrained_feedback_for_form(self, intended_lemma, input_wordform):
		pass

	def get_task_feedback(self, intended_lemma, intended_tags, input_wordform):
		pass

	def __init__(self):
        self.lookup_proc = XFST(
            ERROR_FST_SETTINGS.get('lookup_tool'),
            ERROR_FST_SETTINGS.get('fst_path'),
        )

feedback = FeedbackFST()

@api_view(['GET'])
def hello_world(request):
    print feedback.get_all_feedback_for_form(u'viessui')
    # TODO:
    return Response({"message": "Hello, world!"})

