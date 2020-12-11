from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class WordAdmin(admin.ModelAdmin):
    # list_display = ('id', 'word_en', 'word_ru', 'text_en', 'text_ru', 'audio_en', 'audio_ru', 'wiki_en', 'wiki_ru')
    # search_fields = ('word_en', 'word_ru', 'text_en', 'text_ru',)
    # readonly_fields = ('id', 'audio_en', 'audio_ru', 'wiki_en', 'wiki_ru')
    list_display = ('id', 'word_en',  'text_en',  'audio_en', 'wiki_en', )
    search_fields = ('word_en', 'text_en', )
    readonly_fields = ('id', 'audio_en', 'wiki_en', )
    ordering = ('word_en',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Word, WordAdmin)
