# Generated by Django 4.0.6 on 2022-08-11 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indexpage', '0007_alter_interesting_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('win', models.BooleanField(blank=True, null=True)),
                ('my_org', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.userorgs')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.procedures')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]