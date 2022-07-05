# Generated by Django 2.2.12 on 2022-07-03 09:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkbox', '0004_auto_20220618_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.ManyToManyField(related_name='assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='due',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
