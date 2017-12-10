from django.conf.urls import url
from . import  views
from django.contrib.auth.decorators import login_required
urlpatterns = [

    # /nsns/
    url(r'^$',login_required(views.Boy_Girl_ListView.as_view()),name='nsns'),









]