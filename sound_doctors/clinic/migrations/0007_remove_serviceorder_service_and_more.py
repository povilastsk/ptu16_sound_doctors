# Generated by Django 4.2.7 on 2023-11-14 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_customservice_regularservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='service',
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='custom_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.customservice', verbose_name='custom service'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='regular_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.regularservice', verbose_name='regular service'),
        ),
        migrations.AlterField(
            model_name='servicereview',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_reviews', to='clinic.regularservice', verbose_name='service'),
        ),
        migrations.DeleteModel(
            name='CustomServiceOrder',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
