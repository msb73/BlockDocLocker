# Generated by Django 4.2.6 on 2023-11-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fname',
            field=models.CharField(default='Enter Fname', max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='lname',
            field=models.CharField(default='Enter Lname', max_length=30),
        ),
    ]
