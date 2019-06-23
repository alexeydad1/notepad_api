# Generated by Django 2.2.2 on 2019-06-21 22:57

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notepad', '0002_auto_20190617_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 21, 22, 57, 51, 302141, tzinfo=utc), verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_items', to='notepad.Purchase', verbose_name='Покупка'),
        ),
    ]
