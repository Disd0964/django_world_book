# Generated by Django 5.1.2 on 2025-03-06 18:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_author_borroewr_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.book', verbose_name='Название книги'),
        ),
    ]
