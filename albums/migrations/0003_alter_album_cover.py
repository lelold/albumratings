# Generated by Django 3.2.16 on 2023-01-17 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20230117_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.CharField(default=models.BigAutoField(primary_key=True, serialize=False), max_length=200),
        ),
    ]