"""coursework3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views
from .views import log_in, register, account_api, user_api, profileupdate, createItem, getItemDetail, addBid, getBids, displayItems, search, question, answer
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', log_in),
    path("register/", register, name="register"),
    path("profileupdate/<int:account_id>/", profileupdate),

    # api for account
    path('api/account/', account_api, name='account api'),
    path('api/accounts/<int:account_id>/', user_api,),
    path('item/<int:account_id>/', createItem, name='create Item'),
    path('getItemDetail/<int:item_id>/', getItemDetail, name='create Item'),
    path('addBid/<int:item_id>/', addBid, name='add bid'),
    path('getBids/<int:item_id>/', getBids, name='add bid'),
    path('displayItems/', displayItems, name='displayItems'),
    path('search/', search, name='search'),
    path('question/<int:item_id>/', question, name='question'),
    path('answer/<int:item_id>/', answer, name='answer')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
