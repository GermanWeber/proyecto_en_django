# Generated by Django 5.0.6 on 2024-06-25 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_post_amount_post_img_post_marca_post_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sdName', models.CharField(max_length=50, null=True)),
                ('lastName', models.CharField(max_length=50)),
                ('rut', models.IntegerField(default=11111111)),
                ('DVrut', models.CharField(default=1, max_length=1)),
                ('imgUser', models.ImageField(blank=True, null=True, upload_to='fotos/')),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCompra', models.CharField(max_length=100)),
                ('precioCompra', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compra', to='tienda.post')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compra', to='tienda.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='usuario',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='tienda.usuario'),
            preserve_default=False,
        ),
    ]
