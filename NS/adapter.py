
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from datetime import datetime, timedelta

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        threshold = 90 #seconds

        assert request.user.is_authenticated()
        if (request.user.last_login - request.user.date_joined).seconds < threshold:
            path = "/{user_id}/update/"
            path =  path.format(user_id=request.user.id)
        else:
            path = "/nsns"
        return path
            # url = settings.LOGIN_REDIRECT_URL
        # return resolve_url(url)