# Generated by Django 3.1.7 on 2021-04-12 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0015_auto_20210412_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='tags',
            new_name='taken_tags',
        ),
    ]
