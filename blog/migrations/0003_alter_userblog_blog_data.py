# Generated by Django 4.1.2 on 2022-11-14 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_userblog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userblog',
            name='blog_data',
            field=models.CharField(max_length=800),
        ),
    ]