# Generated by Django 5.1.1 on 2024-11-27 05:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0006_cart_total_cost'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chekout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_address', models.TextField(max_length=500)),
                ('phone_no', models.CharField(max_length=15)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]