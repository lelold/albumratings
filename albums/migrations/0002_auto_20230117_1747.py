# Generated by Django 3.2.16 on 2023-01-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='album',
            name='rating_num',
            field=models.IntegerField(default=0),
        ),
    ]
