# Generated by Django 3.2.15 on 2024-05-29 12:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('pwd', models.CharField(max_length=64)),
                ('nickname', models.CharField(max_length=10)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('signature', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.IntegerField(choices=[(1, '正常'), (0, '封号')], default=1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='account.user')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='account.user')),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
    ]