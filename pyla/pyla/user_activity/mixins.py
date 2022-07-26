import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pyla.manage_profiles.models import ContactUs

class SubmitFeedbackMixin(UserPassesTestMixin):
    def test_func(self):
        feedback_messages = ContactUs.objects.filter(user_id=self.request.user.pk)
        feedback_messages = feedback_messages.filter(status=False)

        if len(feedback_messages) >= 3:
            return render(self.request, 'exception_handling/no-feedback-submit-access.html')

class HandleReplyMixin(UserPassesTestMixin):
    def test_func(self):
        object_pk = self.kwargs['pk']
        feedback = ContactUs.objects.get(pk=object_pk)
        logging.critical(f"{feedback.status}")
        if feedback.status is True:
            return False
        else:
            return True
