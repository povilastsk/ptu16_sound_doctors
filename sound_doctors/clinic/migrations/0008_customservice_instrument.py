# Generated by Django 4.2.7 on 2023-11-14 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_remove_serviceorder_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customservice',
            name='instrument',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.instrument', verbose_name='instrument'),
        ),
    ]
