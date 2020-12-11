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

def translator(OBJ):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    html = requests.get(f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q={OBJ}',
                        headers=HEADERS, params=None)
    if html.status_code == 200:
        arr = []
        word = ''
        for i in html.text:
            arr.append(i)
        for i1 in range(len(arr)):
            if arr[i1] == '"':
                arr = arr[i1:len(arr)]
                i2 = 0
                while not word.endswith('",'):
                    word += arr[i2]
                    i2 += 1
                break
        word = word[1:len(word) - 2]

        return word


def get_clear_text(items, lang):
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
        if lang == "ru":
            if arr[i1] == "◆":
                index = i1
                break
        if arr[i1] == "\n":
            index = i1
            break

    items = items[0:index]
    return items


def get_html(url, HEADERS, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_wikipedia_url(OBJ, lang):
    wiki_wiki = wikipediaapi.Wikipedia(lang)
    page_py = wiki_wiki.page(OBJ)

    if page_py.exists():
        return page_py.fullurl
    else:
        return False


def get_content(html, OBJ, HEADER, HOST, URL, lang):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.ol.get_text()
    meaning = get_clear_text(items, lang)
    audio = soup.find('td', class_='audiometa')
    print(OBJ)
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
        'wikipedia_url': get_wikipedia_url(OBJ, lang),
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


def get_params(word, lang):
    URL = f'https://{lang}.wiktionary.org/wiki/{word}'

    HOST = f'https://{lang}.wiktionary.org/'

    return [URL, HOST]



def get_word(request, word, lang):
    agent_accept = get_header(request)
    if lang == "ru":
        word = translator(word)
    # URL = f'https://en.wiktionary.org/wiki/{word}'
    HEADERS = {'user-agent': agent_accept[0], 'accept': agent_accept[1]}
    # HOST = 'https://en.wiktionary.org/'
    params = get_params(word, lang)
    URL = params[0]
    HOST = params[1]

    html = get_html(URL, HEADERS, None)
    if html.status_code == 200:
        object = get_content(html.text, word, HEADERS, HOST, URL, lang)
        return object
    else:
        return 'Not found'


class Main(View):

    def post(self, request):
        word = request.POST.get('word')
        word_ru = translator(word)
        words = Word.objects.all()
        en_words = []
        for i in words:
            en_words.append(i.word_en)
        if word in en_words:
            return redirect('dict_main_url')
        else:
            en_word = get_word(request, word, 'en')
            ru_word = get_word(request, word, 'ru')
            Word.objects.create(word_en=word,
                                text_en=en_word['meaning'],
                                audio_en=en_word['link_audio'],
                                wiki_en=en_word['wikipedia_url'],
                                pronunciation_en=en_word['pronunciation'],
                                word_ru=word_ru,
                                text_ru=ru_word['meaning'],
                                audio_ru=ru_word['link_audio'],
                                wiki_ru=ru_word['wikipedia_url'],
                                pronunciation_ru=ru_word['pronunciation'],

                                )
        return redirect('dict_main_url')


    def get(self, request):
        words = Word.objects.all()

        return render(request, 'dictionary/Main.html', context={'words': words })