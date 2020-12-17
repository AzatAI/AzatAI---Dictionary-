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
from .serializers import *
import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re
from users_app.forms import *
def translator(OBJ, lang):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    html = requests.get(f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q={OBJ}',
                        headers=HEADERS, params=None)
    if lang == 'en':
        html = requests.get(f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=ru&tl=en&dt=t&q={OBJ}',
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
    words = str(OBJ).split()
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.ol.get_text()
    meaning = get_clear_text(items, lang)
    audio = soup.find('td', class_='audiometa')
    if len(words) > 1:
        pronunciation = OBJ
        link_audio = ""
    else:
        try:
            pronunciation = soup.find('span', class_="IPA").get_text()
        except AttributeError:
            pronunciation = OBJ
        try:
            link = str(audio).split('href="')[1].split('"')[0]
        except IndexError :
            link = ''
        html1 = get_html(HOST+link, HEADER)
        soup1 = BeautifulSoup(html1.text, 'html.parser')
        audio = soup1.find('a', class_='internal')
        try:
            link_audio = 'https:' + str(audio).split('href="')[1].split('"')[0]
        except Exception:
            link_audio = ''

    object = {
        'meaning': meaning,
        'link_audio': link_audio,
        'url': URL,
        'wikipedia_url': get_wikipedia_url(OBJ, lang),
        'pronunciation': pronunciation,

    }
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

    HEADERS = {'user-agent': agent_accept[0], 'accept': agent_accept[1]}
    params = get_params(word, lang)
    URL = params[0]
    HOST = params[1]

    html = get_html(URL, HEADERS, None)
    if html.status_code == 200:
        object = get_content(html.text, word, HEADERS, HOST, URL, lang)
        return object
    else:
        return redirect("not_found_url")


class Main(View):

    def post(self, request):
        if request.POST.get('word'):
            word = str(request.POST.get('word')).lower().strip()
            word.replace(" ", "_")
            if not word:
                return redirect('dict_main_url')
            word_ru = translator(word, 'ru')
            word_en = translator(word, 'en')

            is_ru = (re.findall(r'[а-яА-ЯёЁ]', word))
            words = Word.objects.all()
            en_words = []
            ru_words = []
            lang = 'en'
            for i in words:
                en_words.append(i.word_en)
                ru_words.append(i.word_ru)
            if is_ru:
                lang = 'ru'
                if word_ru in ru_words:
                    word_ru = Word.objects.get(word_ru=word_ru)
                    return redirect('word_detail_url', id=word_ru.id, lang=lang)
            elif word_en in en_words:
                word_en = Word.objects.get(word_en=word_en)
                return redirect('word_detail_url', id=word_en.id, lang=lang)

            en_word = get_word(request, word_en.lower(), 'en')
            ru_word = get_word(request, word_ru.lower(), 'ru')

            try:
                word = Word.objects.create( word_en=word_en,
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
            except Exception:
                return redirect("not_found_url")

            return redirect('word_detail_url', id=word.id, lang=lang)
        return redirect('dict_main_url')


    def get(self, request):
        words = Word.objects.all()
        form = RegistrationForm()
        history_words = []
        if request.user.is_authenticated:
            history_words = HistoryWord.objects.filter(user=request.user)
        return render(request, 'index.html', context={'words': words,'form': form, 'history_words': history_words})


class WordDetail(View):
    def get(self, request, id, lang):
        word = Word.objects.get(id=id)

        if request.user.is_authenticated:
            history_words = HistoryWord.objects.filter(user=request.user)

            his_words_en = []
            his_words_ru = []
            for i in history_words:
                his_words_en.append(i.word.word_en)
                his_words_ru.append(i.word.word_ru)

            if word.word_en not in his_words_en or word.word_ru not in his_words_ru:

                HistoryWord.objects.create(user=request.user, word=word)
            else:
                last_word = HistoryWord.objects.get(user=request.user, word=word)
                last_word.delete()
                HistoryWord.objects.create(user=request.user, word=word)

        return render(request, 'index1.html', context={'word': word, 'lang': lang})

# class WordList(View):
#     def get(self, request, words):
#         arr = []
#         for word in words:
#             arr.append(Word.objects.get(id=word.id))
#         return redirect(request, 'dictionary/world_list.html', context={'words': words})
#

class NotFound(View):
    def get(self, request):
        return render(request, '404.html', )

class WordView(APIView):
    def get(self, request):
        words = Word.objects.all()

        serializer = WordSerializer_v1(words, many=True)

        return Response(serializer.data)



class MyAccount(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('dict_main_url')
        history = HistoryWord.objects.filter(user=request.user)
        if len(history) > 10:
            i = len(history) - 10
            history = history[0:len(history)-i]
        return render(request, 'privatefolder.html', context={'history': history, })


class MyAccountEdit(View):
    def post(self, request):
        user_new_data = Users.objects.get(id=request.user.id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        image = request.FILES.get('image')
        if not image:
            image = request.user.image
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password:
            user = authenticate(email=request.user.email, password=password)
            if user:
                user_new_data.first_name = first_name
                user_new_data.last_name = last_name
                user_new_data.email = email
                user_new_data.image = image
                user_new_data.phone_number = phone_number
                if password1 == password2:
                    user_new_data.set_password(password1)
                    user_new_data.save()
                    new_user = authenticate(email=email, password=password1)
                    login(request, new_user)
        else:
            user_new_data.first_name = first_name
            user_new_data.last_name = last_name
            user_new_data.email = email
            user_new_data.image = image
            user_new_data.phone_number = phone_number
            user_new_data.save()

        return redirect('my_account_url')

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account_edit.html', context={'form': form })