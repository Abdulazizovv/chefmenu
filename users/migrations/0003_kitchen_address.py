# Generated by Django 5.0.3 on 2024-05-05 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_phonenumbers_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]