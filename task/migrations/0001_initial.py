# Generated by Django 4.1.1 on 2022-10-06 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='modelTak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
            ],
            options={
                'verbose_name': 'modelTak',
                'verbose_name_plural': 'modelTaks',
            },
        ),
    ]
