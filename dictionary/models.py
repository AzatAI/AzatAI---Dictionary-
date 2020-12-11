from django.db import models
from users_app.views import set_id, get_hex_id
# Create your models here.


class Word(models.Model):
    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    word_en = models.CharField(max_length=100)
    # word_ru = models.CharField(max_length=30)
    text_en = models.TextField(max_length=30000)
    # text_ru = models.CharField(max_length=3000)
    audio_en = models.CharField(max_length=100)
    # audio_ru = models.CharField(max_length=100)
    wiki_en = models.CharField(max_length=100)
    # wiki_ru = models.CharField(max_length=100)
    pronunciation_en = models.CharField(max_length=100)
    # pronunciation_ru = models.CharField(max_length=100)

    def __str__(self):
        return self.word_en

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = set_id()
        super(Word, self).save(*args, **kwargs)