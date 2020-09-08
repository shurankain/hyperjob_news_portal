import json
import random
from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic.base import View


class MainPageView(View):
    def get(self, request):
        return redirect("/news/")


class NewsView(View):
    def get(self, request, news_id):
        with open(settings.NEWS_JSON_PATH) as json_file:
            news = json.load(json_file)
            for news_item in news:
                if news_item['link'] == int(news_id):
                    return render(
                        request, 'news_page.html', context={
                            'news': news_item
                        }
                    )
            raise Http404


def create_response(dates_sorted_dict, news_item):
    date_time_obj = datetime.strptime(news_item["created"], '%Y-%m-%d %H:%M:%S')
    date_str = date_time_obj.date().strftime('%Y-%m-%d')
    if date_str in dates_sorted_dict.keys():
        dates_sorted_dict[date_str].append(news_item)
    else:
        dates_sorted_dict[date_str] = [news_item]


class AllNewsPageView(View):
    def get(self, request):
        title_filter = request.GET.get('q')
        with open(settings.NEWS_JSON_PATH) as json_file:
            news = json.load(json_file)
            dates_sorted_dict = {}

            for news_item in news:
                if title_filter:
                    if title_filter in str(news_item["title"]):
                        create_response(dates_sorted_dict, news_item)
                else:
                    create_response(dates_sorted_dict, news_item)

            return render(
                request, 'all_news.html', context={
                    'dates_sorted_dict': dates_sorted_dict
                }
            )


news_list = []


class News:
    def __init__(self, title, text, link, created):
        self.created = created
        self.title = title
        self.text = text
        self.link = link



class NewsCreationView(View):
    def get(self, request):
        news_list.clear()
        with open(settings.NEWS_JSON_PATH) as json_file:
            news = json.load(json_file)
            for news_item in news:
                news_list.append(news_item)
        return render(request, "create_news.html")

    def post(self, request):
        title = request.POST.get("title")
        text = request.POST.get("text")

        news = News(title, text, random.randint(0, 1000000), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        news_list.append(news.__dict__)
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json.dump(news_list, json_file)
            return redirect('/news')
