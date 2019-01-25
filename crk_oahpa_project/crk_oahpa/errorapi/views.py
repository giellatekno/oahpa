# -*- encoding: utf-8 -*-
"""

# TODO: doublecheck documentation and update

# Corrections API endpoints

## Language list
### HTTP: GET
### /

The idea with this endpoint is simple: provide list of language codes
that can be used in the correction endpoint.

Parameters:

 * NONE

Returns:

    {
        'languages': [
            {
                'short_name': 'asdf',   // probably an ISO, or ISO+some symbols (sme-SoMe)
                'name': 'français',     // user-friendly name
            },
            {
                'short_name': 'sme',   // probably an ISO, or ISO+some symbols (sme-SoMe)
                'name': 'Davvisámegiella',
            },
            {
                'short_name': 'sme-SoMe',   // probably an ISO, or ISO+some symbols (sme-SoMe)
                'name': 'Davvisámegiella (Sosiála media)',
            },
        ]
    }

## Correction endpoint
### HTTP: POST
### /corrections/

Parameters:

 * **input_language** - ISO/short_name for the language correction FST
 * **wordform** - Input wordform to process
 * **lemma** - (optional) lemma to narrow the corrections

 * **output_language** - (optional) language to display response
   descriptions, if request header is not sufficient (i.e., user chooses
   a separate help language or UI language in the app

Returns:

 * List of potential errors

    {
        'input': {
            'wordform': "asdf",
            'lemma': False|'asdf'
        },
        'suggestions': [
            {
                'name': 'error_tag',
                'description': 'This is an error description',
                'correct_forms': ['wordform1', 'wordform2'],
            },
            {
                'name': 'error_tag_2',
                'description': 'This is an error description',
                'correct_forms': ['wordform1', 'wordform2'],
            },
        ]
    }

"""

import os, sys

from django.conf import settings
from django.shortcuts import render_to_response

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .messages import *
from .processes import FeedbackFST
from .log import ERROR_FST_LOG

ERROR_FST_SETTINGS = settings.ERROR_FST_SETTINGS

_fst_file = ERROR_FST_SETTINGS.get('fst_path')

if not os.path.isfile(_fst_file):
    print >> sys.stderr, "FST file at <%s> does not exist."
    print >> sys.stderr, "Check the path in settings.py and try again."

error_files = ERROR_FST_SETTINGS.get('error_message_files', {}).values()
feedback_messages = FeedbackMessageStore(*error_files)
feedback = FeedbackFST(feedback_messages)

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
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

    # TODO: @tag2 attribute

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
            lookup_query = lookup_query
            response_data = feedback.get_all_feedback_for_form(lookup_query, **message_kwargs)

    return Response(response_data)

def test_page(request):
    return render_to_response('test_page.html')
