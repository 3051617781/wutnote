# Generated by Django 3.2.15 on 2024-05-29 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='notes', to='note.Tag'),
        ),
    ]
