# Generated by Django 5.0.6 on 2024-07-16 22:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0025_remove_transaccioncompra_fechatran'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccioncompra',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]