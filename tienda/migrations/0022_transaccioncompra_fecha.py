# Generated by Django 5.0.6 on 2024-06-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0021_alter_post_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccioncompra',
            name='fecha',
            field=models.IntegerField(default=0),
        ),
    ]