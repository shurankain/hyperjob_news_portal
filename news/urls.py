from django.urls import path
from django.conf.urls import url

from .views import MainPageView, NewsView, AllNewsPageView, NewsCreationView

urlpatterns = [
    path('', MainPageView.as_view()),
    path('news/', AllNewsPageView.as_view()),
    path('news/create/', NewsCreationView.as_view()),
    url(r'^news/(?P<news_id>[0-9]+)/$', NewsView.as_view())
]
