# Generated by Django 3.2.16 on 2023-01-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0005_auto_20230117_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='rating_all',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
