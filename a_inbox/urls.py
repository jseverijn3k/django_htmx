from django.urls import path

from a_inbox.views import *

urlpatterns = [

    # a_inbox urls
    path('', inbox_view, name='inbox'),

    ]

