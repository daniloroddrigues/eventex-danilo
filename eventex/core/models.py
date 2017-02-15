from django.db import models
from django.shortcuts import resolve_url as r

from eventex.core.managers import KindQuerySet, PeriodManager


class Speaker(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    website = models.URLField('website', blank=True)
    photo = models.URLField('foto')
    description = models.TextField('descriçao', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'
    KINDS = (
        (EMAIL, 'Email'),
        (PHONE, 'Telefone')
    )
    speaker = models.ForeignKey('Speaker', verbose_name='palestrante')
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)

    # Meta programaçao - instancia um manager a partir do meu queryset,
    # - isso acontece quando meu queryset esta muito alinhado com manager.
    objects = KindQuerySet().as_manager()

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.value


class Talk(models.Model):
    title = models.CharField('titulo', max_length=200)
    start = models.TimeField('inicio', blank=True, null=True)
    description = models.TextField('descriçao', blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='palestrantes', blank=True)

    objects = PeriodManager()

    class Meta:
        verbose_name = 'palestra'
        verbose_name_plural = 'palestras'

    def __str__(self):
        return self.title
