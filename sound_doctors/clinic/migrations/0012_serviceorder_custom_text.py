# Generated by Django 4.2.7 on 2023-11-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0011_alter_serviceorder_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='custom_text',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='custom text'),
        ),
    ]
