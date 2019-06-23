from django.db import models
from django.utils import timezone


class Purchase(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя')
    name = models.CharField(verbose_name='Название покупки', max_length=128)
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        return self.name


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items', verbose_name='Покупка', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название продукта / предмета', max_length=128)
    is_buy = models.BooleanField(verbose_name='Куплено', default=False)

    class Meta:
        verbose_name = 'Список продуктов / предметов'
        verbose_name_plural = 'Списки продуктов / предметов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя')
    name = models.CharField(verbose_name='Заголовок', max_length=128)
    content = models.TextField(verbose_name='Содержание')
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Event(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя')
    created = models.DateTimeField(verbose_name='Время создания', default=timezone.now)
    name = models.CharField(verbose_name='Название события', max_length=128)
    description = models.TextField(verbose_name='Описание')
    end_date = models.DateTimeField(verbose_name='Дата окончания события')
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['end_date']

    def __str__(self):
        return self.name


class CountAccess(models.Model):
    counter = models.PositiveIntegerField(default=0)