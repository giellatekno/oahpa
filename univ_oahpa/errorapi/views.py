# -*- encoding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .messages import *
from .processes import XFST
from .log import ERROR_FST_LOG

import simplejson

ERROR_FST_SETTINGS = settings.ERROR_FST_SETTINGS

class FeedbackFST(object):

    def _error_tags_from_fst(self, fst_response):
        """ Grab the error tags returned in the FST response, based on
        the tags available in the message store.
        """

        error_tags = []
        for wf, analyses in fst_response:
            for lem, tag in analyses:
                # TODO: tagsets instead?
                existing_errors = \
                    set(tag) & set(self.message_store.error_tags)
                error_tags.extend(existing_errors)

        error_tags = list(set(error_tags))

        return error_tags

    def _messages_for_error_tags(self, error_tags, display_lang, task=False):
        error_messages = []

        # TODO: replace WORDFORM with input_wordform

        for err_tag in error_tags:
            if task:
                message = self.message_store.get_message(display_lang, err_tag, task=task)
            else:
                message = self.message_store.get_message(display_lang, err_tag)
            error_messages.append({
                'tag': err_tag,
                'message': message
            })

        return error_messages

    def get_all_feedback_for_form(self, input_wordform, task=False,
                                  intended_lemma=False, display_lang='nob'):
        """ Accepts a wordform, returns feedback error tags and
        messages.
        """
        fst_response = self.lookup_proc.lookup([input_wordform])

        if intended_lemma:

            def lemma_filter((wf, analyses)):
                for lem, tag in analyses:
                    if lem == intended_lemma:
                        return (wf, analyses)

            fst_response = filter(lemma_filter, fst_response)

        error_tags = self._error_tags_from_fst(fst_response)

        error_messages = self._messages_for_error_tags(error_tags, display_lang, task=task)

        return {
            'fst': fst_response,
            'error_tags': error_tags,
            'messages': error_messages
        }

    def __init__(self, message_store):
        self.lookup_proc = XFST(
            ERROR_FST_SETTINGS.get('lookup_tool'),
            ERROR_FST_SETTINGS.get('fst_path'),
        )
        self.message_store = message_store

error_files = ERROR_FST_SETTINGS.get('error_message_files', {}).values()
feedback_messages = FeedbackMessageStore(*error_files)
feedback = FeedbackFST(feedback_messages)

@api_view(['GET', 'POST'])
def error_feedback_view(request):
    """ Error lookup view takes a JSON object containing the following
    parameters:

        @param lookup (string) - this is the input wordform wordform

    Optional parameters:

        @param task (string) - this is the task the user is aiming for: Pl+Acc
        @param intended_lemma (string) - This constrains the feedback to
            only specific lemmas. I.e., the user enters 'viessu', so we
            are not interested in forms of the word 'viessat', just
            forms of the word 'viessu'.

    Example:
        {"lookup": "viessui", "task": "Pl+Acc"}

    TODO: options method that returns all possible error tags, and
    task strings.

    """

    # TODO: include the task
    # TODO: @tag2 attribute
    # TODO: template tag for including all the script/css prerequisites
    # in other modules (i.e., univ_drill). f.ex.: 
    #    {% errorapi_scripts %}

    response_data = {
        'success': False,
    }

    if request.POST:
        response_data = {
            'success': True,
        }

        lookup_query = request.DATA.get('lookup', False)
        task = request.DATA.get('task', False)
        intended_lemma = request.DATA.get('intended_lemma', False)

        message_kwargs = {
            'display_lang': 'nob',
        }

        if task:
            message_kwargs['task'] = task
        if intended_lemma:
            message_kwargs['intended_lemma'] = intended_lemma

        if lookup_query:
            lookup_query = lookup_query.decode('utf-8')
            response_data = feedback.get_all_feedback_for_form(lookup_query, **message_kwargs)

    return Response(response_data)

def test_page(request):
	return render_to_response('test_page.html')
