# Generated by Django 5.0.6 on 2024-06-09 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation_app', '0006_rename_message_message_messageid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turnstile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isCompleted', models.BooleanField(default=False)),
            ],
        ),
    ]