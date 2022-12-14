# Generated by Django 4.1.2 on 2022-12-01 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0)),
                ('wishlist_prd_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.productinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_prd_quantity', models.BigIntegerField()),
                ('cart_total_price', models.BigIntegerField()),
                ('user_id', models.BigIntegerField()),
                ('cart_prd_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.productinfo')),
            ],
        ),
    ]
