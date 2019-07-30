import re
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseForbidden
from employee.models import Profile

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

        self.exceptions = tuple(re.compile(url)
                                for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):

        auth_url_run = True

        if request.user.is_authenticated:
            request.profile = Profile.objects.get(user=request.user)

        for url in self.exceptions:
            if url.match(request.path):
                auth_url_run = False
        
        response = self.get_response(request)
        if not request.user.is_authenticated and auth_url_run :
            return HttpResponseRedirect('/login')    
        
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        for url in self.exceptions:
            if url.match(request.path):
                return None