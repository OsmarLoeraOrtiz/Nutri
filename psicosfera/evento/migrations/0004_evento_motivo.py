# Generated by Django 3.2.23 on 2024-02-02 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0003_notification_notification_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='motivo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]