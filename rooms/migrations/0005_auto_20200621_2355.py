# Generated by Django 2.2.5 on 2020-06-21 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200618_0459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='adddress',
            new_name='address',
        ),
    ]