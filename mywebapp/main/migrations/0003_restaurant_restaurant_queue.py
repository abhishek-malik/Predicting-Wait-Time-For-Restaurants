# Generated by Django 2.2 on 2019-04-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190415_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_queue',
            field=models.IntegerField(default=0),
        ),
    ]
