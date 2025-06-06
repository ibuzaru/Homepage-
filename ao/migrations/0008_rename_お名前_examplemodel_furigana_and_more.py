# Generated by Django 5.1.4 on 2024-12-31 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ao', '0007_examplemodel_電話番号'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examplemodel',
            old_name='お名前',
            new_name='furigana',
        ),
        migrations.RenameField(
            model_name='examplemodel',
            old_name='フリガナ',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='examplemodel',
            old_name='電話番号',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='examplemodel',
            name='メールアドレス',
        ),
        migrations.AddField(
            model_name='examplemodel',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='examplemodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='examplemodel',
            name='postal_code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
