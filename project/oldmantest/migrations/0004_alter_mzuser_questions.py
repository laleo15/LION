# Generated by Django 4.2.1 on 2023-08-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oldmantest', '0003_alter_mzuser_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mzuser',
            name='questions',
            field=models.JSONField(default=dict),
        ),
    ]
