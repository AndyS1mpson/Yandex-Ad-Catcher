# Generated by Django 4.0.5 on 2022-07-12 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsejob',
            name='start_parse',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]