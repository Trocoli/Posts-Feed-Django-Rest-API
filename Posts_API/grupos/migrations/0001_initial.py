# Generated by Django 3.2.8 on 2021-12-20 19:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=11)),
                ('slug', models.SlugField(unique=True)),
                ('users', models.ManyToManyField(related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'ordering': ['-id'],
            },
        ),
    ]
