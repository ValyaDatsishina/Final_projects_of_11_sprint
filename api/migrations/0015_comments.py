# Generated by Django 3.0.5 on 2021-06-29 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210625_0615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Review')),
                ('title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Titles')),
            ],
        ),
    ]
