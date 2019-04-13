import datetime

"""
Django provides a test Client to simulate a user interacting with the code at the view level. We can use it in tests.py or even in the shell.

>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()

setup_test_environment() installs a template renderer which will allow us to examine some additional attributes on responses such as response.context that otherwise wouldn’t be available. Note that this method does not setup a test database, so the following will be run against the existing database and the output may differ slightly depending on what questions you already created. You might get unexpected results if your TIME_ZONE in settings.py isn’t correct. If you don’t remember setting it earlier, check it before continuing.
"""

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was published_recently() returns False for questions whose pub_date is in the future
        """

        """
        What happened is this:

        manage.py test polls looked for tests in the polls application
        it found a subclass of the django.test.TestCase class
        it created a special database for the purpose of testing
        it looked for test methods - ones whose names begin with test
        in test_was_published_recently_with_future_question it created a Question instance whose pub_date field is 30 days in the future
        … and using the assertIs() method, it discovered that its was_published_recently() returns True, though we wanted it to return False
        The test informs us which test failed and even the line on which the failure occurred.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
