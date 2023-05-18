# Generated by Django 4.1.7 on 2023-05-16 06:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_cart_carts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('Id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='books',
            name='Category',
        ),
        migrations.AddField(
            model_name='books',
            name='CategoryId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.categories'),
            preserve_default=False,
        ),
    ]