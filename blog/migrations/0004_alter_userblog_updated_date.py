# Generated by Django 4.1.2 on 2022-11-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_userblog_blog_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userblog',
            name='updated_date',
            field=models.DateTimeField(),
        ),
    ]