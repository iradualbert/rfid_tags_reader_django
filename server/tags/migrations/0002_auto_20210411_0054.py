# Generated by Django 3.1.7 on 2021-04-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag_name',
            new_name='tag_id',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='has_left',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='last_time_left',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='last_time_taken',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='recent_user',
        ),
        migrations.AddField(
            model_name='entry',
            name='reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='profile',
            name='on_board',
            field=models.BooleanField(default=False),
        ),
    ]
