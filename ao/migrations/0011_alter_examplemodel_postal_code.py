# Generated by Django 5.1.4 on 2025-01-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ao', '0010_examplemodel_check_in_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examplemodel',
            name='postal_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
