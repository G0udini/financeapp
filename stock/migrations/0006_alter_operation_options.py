# Generated by Django 4.0 on 2022-01-05 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_alter_operation_share'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operation',
            options={'ordering': ['-date']},
        ),
    ]
