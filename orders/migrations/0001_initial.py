# Generated by Django 5.0.3 on 2024-05-05 02:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.food')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default=uuid.uuid4, editable=False, max_length=10, unique=True)),
                ('total_price', models.IntegerField()),
                ('status', models.CharField(choices=[('new', 'Yangi'), ('in_progress', 'Ishlanmoqda'), ('done', 'Bajarildi')], default='new', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('foods', models.ManyToManyField(to='orders.orderitems')),
            ],
            options={
                'verbose_name': 'Buyurtma',
                'verbose_name_plural': 'Buyurtmalar',
            },
        ),
    ]