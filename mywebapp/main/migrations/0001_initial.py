# Generated by Django 2.2 on 2019-04-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=200)),
                ('restaurant_distance', models.CharField(max_length=200)),
                ('restaurant_rating', models.IntegerField()),
                ('restaurant_wait', models.FloatField()),
            ],
        ),
    ]