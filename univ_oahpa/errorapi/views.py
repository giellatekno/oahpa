from django.conf import settings

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .processes import XFST
from .log import ERROR_FST_LOG

import simplejson

ERROR_FST_SETTINGS = settings.ERROR_FST_SETTINGS

class FeedbackMessageStore(object):
    """ Reads and stores messages in memory.
    """

    # Example of format. This will be rewritten on file load.
    messages = {
        'sme': {
            'CGErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "CGErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "CGErr",
                },
            ],
            'DiphErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "DiphErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "DiphErr",
                },
            ],
        },
        'nob': {
            'CGErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "CGErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "CGErr",
                },
            ],
            'DiphErr': [
                {
                    "string": "Message string.",
                    "task": "Sg+Gen",
                    "tag": "DiphErr",
                },
                {
                    "string": "Message string.",
                    "task": "Sg+Loc",
                    "tag": "DiphErr",
                },
            ],
        },
    }

    @property
    def error_tags(self):
        if not hasattr(self, '_error_tags'):
            # Extract tags we care about from XML
            self._error_tags = ['CGErr', 'DiphErr']
        return self._error_tags

    def get_message(self, iso, error_tag, task=False):
        """
            >>> messagestore.get_message("sme", "CGErr")
            "You forgot consonant gradation!"
            >>> messagestore.get_message("sme", "CGErr", task="Sg+Gen")
            "You forgot consonant gradation (genitive sg.)!"
        """

        message = self.messages.get(iso, {}).get(error_tag, error_tag)

        return message

    def parse(self):
        """ Reads the XML file and stores all messages """
        # TODO:

        return

    def __init__(self, xml_path):
        self.path = xml_path
        self.parse()
        # TODO:

class FeedbackFST(object):

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
feedback_messages = FeedbackMessageStore('xmlfile.xml')

@api_view(['GET', 'POST'])
def error_feedback_view(request):
    response_data = {
        'success': False,
    }

    if request.POST:
        response_data = {
            'success': True,
        }
        lookup_query = request.DATA.get('lookup', False)
        if lookup_query:
            results = feedback.get_all_feedback_for_form(lookup_query.decode('utf-8'))
            response_data['fst'] = results

            error_tags = []
            for wf, analyses in results:
                for lem, tag in analyses:
                    # TODO: tagsets instead?
                    error_tags.extend(
                        set(tag) & set(feedback_messages.error_tags)
                    )

            response_data['error_tags'] = error_tags

            error_tags = list(set(error_tags))

            response_messages = []
            for err_tag in error_tags:
                message = feedback_messages.get_message('nob', err_tag)
                
                response_messages.append({
                    'tag': err_tag,
                    'message': message
                })

            response_data['messages'] = response_messages

    return Response(response_data)

