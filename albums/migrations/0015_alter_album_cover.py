# Generated by Django 3.2.16 on 2023-01-20 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0014_alter_album_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.IntegerField(default=models.BigAutoField(primary_key=True, serialize=False)),
        ),
    ]
