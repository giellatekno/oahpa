"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from rest_framework.test import APIRequestFactory

# TODO: create tests for the following procedure

# log in 

    # http --session=courses_test get http://localhost:8000/davvi/courses/standard_login/ | grep csrfmiddlewaretoken | head -n 1 | grep -o "value='\(.*\)'" | sed 's/value=//' | tr -d "'" > token.tmp
    # http -f --session=courses_test POST http://localhost:8000/davvi/courses/standard_login/ username=asdf password=asdf csrfmiddlewaretoken=`cat token.tmp`


# list goals for referer

    # http --session=courses_test GET http://localhost:8000/davvi/courses/api/submission/ Referer:"localhost"

# Log the first action

    # http --session=courses_test --json POST http://localhost:8000/davvi/courses/api/submission/ user_input=blahblah correct=asdf,bbq iscorrect=True task_id=91


    # http --verbose --session=courses_test --json POST http://localhost:8000/davvi/courses/api/submission/ Referer:localhost X-CSRFToken:`cat token.tmp` user_input=blahblah correct=asdf,bbq iscorrect=True task_id=91



class SimpleTest(TestCase):

    def test_submission(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
        factory = APIRequestFactory()

        test_data = {
            'task_id': self.test_task.id
            'is_correct': True,
            'user_input': "asdf bbq",
        }

        # TODO: test referer?
        factory.post('/courses/submission/', test_data, format='json')

