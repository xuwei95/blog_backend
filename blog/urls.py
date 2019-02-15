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
from django.conf.urls import url
from myadmin import views as admin_views
from app import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    url(r'^info/', views.Info.as_view()),
    url(r'^article_list/', views.Article_list.as_view()),
    url(r'^serach/', views.Serach.as_view()),
    url(r'^article_hot/', views.Article_hot.as_view()),
    url(r'^article_category/', views.Article_category.as_view()),
    url(r'^detail/', views.Article_detail.as_view()),
    url(r'^article_detail/', views.Article_detail.as_view()),
    url(r'^admin_login/', admin_views.Login.as_view()),
    url(r'^api_auth_refresh/', refresh_jwt_token),
    url(r'^api_auth_verify/', verify_jwt_token),
    url(r'^api_auth/', obtain_jwt_token),
    url(r'^user/', admin_views.User_list.as_view()),
    url(r'^user_info/', admin_views.User_info.as_view()),
    url(r'^user_setting/', admin_views.User_setting.as_view()),
    url(r'^user_password/', admin_views.User_password.as_view()),
    url(r'^website/', admin_views.Web_site.as_view()),
    url(r'^email/', admin_views.Email.as_view()),
    url(r'^category/', admin_views.Category_list.as_view()),
    url(r'^category_add/', admin_views.Category_add.as_view()),
    url(r'^category_edit/', admin_views.Category_edit.as_view()),
    url(r'^category_del/', admin_views.Category_del.as_view()),
    url(r'^article/', admin_views.Article_list.as_view()),
    url(r'^article_add/', admin_views.Article_add.as_view()),
    url(r'^article_del/', admin_views.Article_del.as_view()),
    url(r'^comments/', admin_views.Comments_list.as_view()),
    url(r'^recly/', admin_views.Recly_list.as_view()),
    url(r'^syslog/', admin_views.Syslog_list.as_view()),
    url(r'^userlog/', admin_views.Userlog_list.as_view()),
]
