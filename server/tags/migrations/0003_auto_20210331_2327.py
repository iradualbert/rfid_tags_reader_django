# Generated by Django 3.1.7 on 2021-03-31 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_entry_antenna'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
