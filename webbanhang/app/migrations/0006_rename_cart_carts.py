# Generated by Django 4.1.7 on 2023-05-16 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_books_cart_persons_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='Carts',
        ),
    ]
