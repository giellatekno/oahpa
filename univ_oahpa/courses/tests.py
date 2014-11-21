"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from rest_framework.test import APIRequestFactory



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

