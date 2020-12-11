from django.shortcuts import render
import platform
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from django.contrib.auth import login, authenticate, logout
from .models import *
import user_agents
# from .forms import *
# from .serializers import *
# import re
# from .utils import *
from django.core.exceptions import *
import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re


def get_clear_text(items):
    i = 0
    items_arr = []
    for i1 in items:
        items_arr.append(i1)

    while i < len(items):
        if items_arr[i] == '[':
            while items_arr[i] != ']':
                items_arr[i] = ''
                i += 1
            if items_arr[i] == ']':
                items_arr[i] = ''

        i += 1
        items = ''
        for i2 in items_arr:
            items += i2

    arr = []
    index = 0
    for i in items:
        arr.append(i)
    for i1 in range(len(arr)):
        if arr[i1] == "\n":
            index = i1
            break

    items = items[0:index]
    return items


def get_html(url, HEADERS, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_wikipedia_url(OBJ):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(OBJ)

    if page_py.exists():
        return page_py.fullurl
    else:
        return False


def get_content(html, OBJ, HEADER, HOST, URL):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.ol.get_text()
    meaning = get_clear_text(items)
    audio = soup.find('td', class_='audiometa')
    pronunciation = soup.find('span', class_="IPA").get_text()
    link = str(audio).split('href="')[1].split('"')[0]
    html1 = get_html(HOST+link, HEADER)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    audio = soup1.find('a', class_='internal')
    link_audio = 'https:' + str(audio).split('href="')[1].split('"')[0]

    object = {
        'meaning': meaning,
        'link_audio': link_audio,
        'url': URL,
        'wikipedia_url': get_wikipedia_url(OBJ),
        'pronunciation': pronunciation,

    }
    print(object)
    return object


def get_header(request):
    agent_accept = []
    regex = re.compile('^HTTP_')
    head = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))
    agent_accept.append(head['USER_AGENT'])
    agent_accept.append(head['ACCEPT'])
    return agent_accept

def get_word(request, word, lang):
    agent_accept = get_header(request)
    URL = f'https://en.wiktionary.org/wiki/{word}'
    HEADERS = {'user-agent': agent_accept[0], 'accept': agent_accept[1]}
    HOST = 'https://en.wiktionary.org/'
    html = get_html(URL, HEADERS, None)
    if html.status_code == 200:
        object = get_content(html.text, word, HEADERS, HOST, URL)
        return object
    else:
        return 'Not found'


class Main(View):

    def post(self, request):
        word = request.POST.get('word')
        words = Word.objects.all()
        en_words = []
        for i in words:
            en_words.append(i.word_en)
        if word in en_words:
            return redirect('dict_main_url')
        else:
            en_word = get_word(request, word, 'en')
            # ru_word = get_word(request, word, 'ru')
            Word.objects.create(word_en=word, text_en=en_word['meaning'], audio_en=en_word['link_audio'], wiki_en=en_word['wikipedia_url'], pronunciation_en=en_word['pronunciation'])
        return redirect('dict_main_url')


    def get(self, request):
        words = Word.objects.all()

        return render(request, 'dictionary/Main.html', context={'words': words })