# Generated by Django 3.2.23 on 2024-01-02 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]