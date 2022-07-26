from django.http import HttpResponse
from django.shortcuts import render
import logging
from pyla.settings import DEBUG


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        DEBUG = True
        if not DEBUG:

            if response.status_code >= 400:
                if response.status_code == 403:
                    return render(request, 'exception_handling/403.html')
                elif response.status_code == 404:
                    logging.error("USER TRIED ACCESSING NON EXISTING PAGE")
                    return render(request, 'exception_handling/404.html')

        return response

    return middleware