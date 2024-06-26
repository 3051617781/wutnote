# Generated by Django 3.2.15 on 2024-05-29 12:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tagname', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotebookColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('abstract', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('browse_num', models.BigIntegerField(default=0)),
                ('favor_num', models.BigIntegerField(default=0)),
                ('collect_num', models.BigIntegerField(default=0)),
                ('visibility', models.IntegerField(choices=[(1, '公开'), (0, '私有')], default=1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('column', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='note.notebookcolumn')),
                ('tags', models.ManyToManyField(related_name='notes', to='note.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserFavoriteNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='note.note')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='account.user')),
            ],
            options={
                'unique_together': {('user', 'note')},
            },
        ),
    ]
