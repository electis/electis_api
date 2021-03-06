# Generated by Django 3.1.3 on 2020-11-19 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20201118_0843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='data_fields',
        ),
        migrations.AddField(
            model_name='service',
            name='data',
            field=models.JSONField(blank=True, default=dict, help_text='service (application) data'),
        ),
        migrations.AlterField(
            model_name='messageservicestatus',
            name='posted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='profileservicedata',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='profileservicedata',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='profileservicedata',
            name='token',
        ),
    ]
