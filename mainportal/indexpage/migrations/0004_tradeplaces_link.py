# Generated by Django 4.0.2 on 2022-04-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0003_procedures_proc_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeplaces',
            name='link',
            field=models.CharField(default=0, max_length=521),
            preserve_default=False,
        ),
    ]