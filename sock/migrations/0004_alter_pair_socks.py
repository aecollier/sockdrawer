# Generated by Django 4.0.5 on 2022-07-05 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sock', '0003_pair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='socks',
            field=models.JSONField(),
        ),
    ]