# Generated by Django 3.2.16 on 2023-01-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0006_album_rating_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='rating',
            field=models.FloatField(),
        ),
    ]
