# Generated by Django 2.2.12 on 2022-04-26 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('starting', models.FloatField()),
                ('image', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('category', models.CharField(max_length=80)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_item', to='auctions.Auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pub', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('new_comment', models.TextField()),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_item', to='auctions.Auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_bid', models.FloatField()),
                ('count', models.IntegerField(default=1)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_item', to='auctions.Auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidding_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
