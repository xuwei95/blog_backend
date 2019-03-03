"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from myadmin import views as admin_views
from app import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    url(r'^api/(?P<version>[v1]+)/info/$', views.Info.as_view()),
    url(r'^api/(?P<version>[v1]+)/user/$', views.User_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/user/auth/$', obtain_jwt_token),
    url(r'^api/(?P<version>[v1]+)/user/verify/$', verify_jwt_token),
    url(r'^api/(?P<version>[v1]+)/comments/$', views.Comments_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/article/list/$', views.Article_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/article/hot/$', views.Article_hot.as_view()),
    url(r'^api/(?P<version>[v1]+)/article/detail/$', views.Article_detail.as_view()),
    url(r'^api/(?P<version>[v1]+)/serach/', views.Serach.as_view()),
    url(r'^api/(?P<version>[v1]+)/category/$', views.Category_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/auth/$', obtain_jwt_token),
    url(r'^api/(?P<version>[v1]+)/admin/info/$', admin_views.Info.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/user/$', admin_views.Admin_User.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/user/password/$', admin_views.User_password.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/user/list/$', admin_views.User_list.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/comments/$', admin_views.Comments_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/article/$', admin_views.Article_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/recly/$', admin_views.Recly.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/category/$', admin_views.Category_api.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/website/$', admin_views.Web_site.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/email/$', admin_views.Email.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/sys_log/$', admin_views.Syslog.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/sys_info/$', admin_views.Sys_info.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/network_info/$', admin_views.Network_info.as_view()),
    url(r'^api/(?P<version>[v1]+)/admin/user_log/$', admin_views.Userlog.as_view()),
    # path('', include('social_django.urls', namespace='social'))
]
