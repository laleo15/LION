# Generated by Django 4.2.1 on 2023-08-09 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oldmantest', '0006_mzuser_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=100)),
                ('Fone', models.CharField(max_length=200)),
                ('Ftwo', models.CharField(max_length=200)),
                ('Fthird', models.CharField(max_length=200)),
            ],
        ),
    ]