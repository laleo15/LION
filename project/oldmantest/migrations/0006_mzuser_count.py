# Generated by Django 4.2.1 on 2023-08-09 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oldmantest', '0005_testquestion_plgm_testquestion_plgx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mzuser',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
