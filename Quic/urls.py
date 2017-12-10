"""Quic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from niji import urls as niji_urls
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.views import  password_change,password_change_done
from NS import views
from  django.conf import settings
from django.conf.urls.static import static
from  rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as drf_views
from  django.contrib.auth  import  views as auth_view
from  NS import  weixinViews


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nsns/', include('NS.url')),
    url(r'^fellow',  login_required(views.FellowView.as_view()), name='fellow'),

    url(r'^accounts/', include('allauth.urls')),

    # url(r'^fellow(?P<qq>.*)',  login_required(views.FellowView.as_view()), name='fellow'),

    # website:/777/
    url(r'^(?P<slug>[0-9]+)/$', login_required(views.UserDetailView.as_view()), name='detail'),

    # url(r'^community', Community,name='community'),

    # website:/777/add_info
    url(r'^(?P<pk>[0-9]+)/add', views.UserDetailCreate.as_view(), name='userdetail-add'),
    url(r'^(?P<user_id>[0-9]+)/update', views.UserDetailUpdate.as_view(), name='userdetail-update'),



    #/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),




    #comunity

    url(r'^comunity/', include(niji_urls, namespace="niji")),




    #JOSN
    url(r'^all-nsns',views.UserDetailList.as_view(),name='nsns-api'),

    # url(r'^login/$',views.Login,name='login'),
    url(r'^logout/$',views.Logout,name='logout'),
    url(r'^$',views.Home,name='home'),
    url(r'^blog/$',views.Blog),

    # url('^', include('django.contrib.auth.urls')),


    url('^jq-service-api/want2like/', views.like_some),
    url('^jq-service-api/all-id-like-count/', views.get_all_user_like_count),
    url('^jq-service-api/getLoginUserLove/', views.getLoginUserLove),

    url('^jq-service-api/getWhoLoveUser/', views.getWhoLoveUser),
    url('^jq-service-api/getUserMatch/', views.getLoginUserLove),
    url('^jq-service-api/getUserLoveDetail/', views.getUserLoveDetail),
    url('^jq-service-api/getMatched', views.getLoverMatched),




    #weixin api
    url(r'^api-uid-token/', views.CustomObtainAuthToken.as_view()),
    url(r'^api-token-auth/', drf_views.obtain_auth_token),

    # url(r'weixin_update/(?P<token>.*)',views.WeixinUpdatePageView.as_view()),
    url(r'weixin_update/(?P<token>.*)',views.WeiXin_UserDetailUpdate.as_view()),
    url(r'weixin-success',views.SuccessView.as_view()),

    url(r'weixin_createuser/(?P<superToken>.*)',views.CreateUserView.as_view()),
#    url(r'^weixin_api/update/(?P<update_userid>\d+)',views.UserDetailWeiXin.as_view(),name='weixin-djangoRESTAPI'),



    url(r'^top-secret/weixin_account_logger/(?P<superToken>.*)',views.WechatAccountLogView.as_view()),

    url(r'^superuser-id2token-api',views.weixin_superuserToken_get_id),



    url(r'^weixin-user-like',weixinViews.getUserLoveDetail),
    url(r'^weixin-like-user',weixinViews.getWhoLoveUser),
    url(r'^weixin-matched',weixinViews.getLoverMatched),
    url(r'^weixin-like-some',weixinViews.like_some),

    url(r'^check-user-exits',views.Edit_user_info),
    url(r'^weixin-getMetched',weixinViews.getLoverMatched),
    url(r'^check-user-active',views.check_Activate),


    url(r'^develop/province-data-api',views.province_data_vitualiazation),
    url(r'^map',views.MapPageView.as_view())


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
