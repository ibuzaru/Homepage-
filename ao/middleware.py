# redirects_app/middleware.py
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class OldDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.old_domain = 'sanso-ao-glamping-027217be6a65.herokuapp.com'
        self.new_domain = 'www.sansoao.com'

    def __call__(self, request):
        if request.get_host() == self.old_domain:
            new_url = f"{'https' if request.is_secure() else 'http'}://{self.new_domain}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)