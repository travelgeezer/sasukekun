from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

from .models import crawler_news, find_banner_node


def response_json(data):
    response = {
      'code': 0,
      'data': data,
      'info': 'ok!'
    }
    return json.dumps(response, ensure_ascii=False)

def index(request):
    return HttpResponse('hello carwler')

def banner(request):
    soup = crawler_news()
    banner = soup.find_all('div', 'slide-item')
    banner_datas = find_banner_node(banner)
    return HttpResponse(response_json(banner_datas))
