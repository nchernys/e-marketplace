# Generated by Django 4.2.6 on 2024-02-14 06:01

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('new_shop', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_shop.category')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_shop.product')),
            ],
            managers=[
                ('categoryproduct_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AddCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default='0')),
                ('client', models.CharField(max_length=100)),
                ('product_id', models.ManyToManyField(related_name='products', to='new_shop.product')),
            ],
            managers=[
                ('cart_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
