# Generated by Django 4.1.7 on 2023-05-18 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_books_sellnumber_alter_books_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModelBooks',
            fields=[
                ('books_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.books')),
            ],
            bases=('app.books',),
        ),
    ]
