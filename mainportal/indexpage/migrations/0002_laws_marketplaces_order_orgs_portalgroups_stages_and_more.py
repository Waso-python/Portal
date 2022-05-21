# Generated by Django 4.0.2 on 2022-04-06 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laws',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'laws',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Marketplaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('link', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'marketplaces',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_proc', models.CharField(max_length=10)),
                ('link_proc', models.CharField(max_length=500)),
                ('partner', models.CharField(max_length=512)),
                ('summ_proc', models.IntegerField()),
                ('count_order', models.IntegerField()),
                ('subj_proc', models.CharField(max_length=512)),
                ('actual_for_me', models.IntegerField(choices=[(0, 'не актуально'), (1, 'актуально')])),
                ('end_date', models.DateTimeField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=512, null=True)),
                ('short_name', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.CharField(blank=True, max_length=512, null=True)),
                ('phone', models.CharField(blank=True, max_length=512, null=True)),
                ('url', models.CharField(blank=True, max_length=512, null=True)),
                ('inn', models.CharField(blank=True, max_length=512, null=True)),
                ('cod_reestr', models.CharField(blank=True, max_length=512, null=True)),
                ('date_reg', models.DateTimeField(blank=True, null=True)),
                ('date_last_change', models.DateTimeField(blank=True, null=True)),
                ('kpp', models.CharField(blank=True, max_length=512, null=True)),
                ('ogrn', models.CharField(blank=True, max_length=512, null=True)),
                ('oktmo', models.CharField(blank=True, max_length=512, null=True)),
                ('iku', models.CharField(blank=True, max_length=512, null=True)),
                ('date_iku', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'orgs',
            },
        ),
        migrations.CreateModel(
            name='PortalGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'portal_groups',
            },
        ),
        migrations.CreateModel(
            name='Stages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'stages',
            },
        ),
        migrations.CreateModel(
            name='Tradeplaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'tradeplaces',
            },
        ),
        migrations.CreateModel(
            name='TypesProc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'types_proc',
            },
        ),
        migrations.CreateModel(
            name='Procedures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=512, null=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('date_proc', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('law', models.ForeignKey(db_column='law', on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.laws')),
                ('orgs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.orgs')),
                ('places', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.marketplaces')),
                ('stage', models.ForeignKey(db_column='stage', on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.stages')),
                ('tradeplace', models.ForeignKey(db_column='tradeplace', on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.tradeplaces')),
                ('type_proc', models.ForeignKey(db_column='type_proc', on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.typesproc')),
            ],
            options={
                'db_table': 'procedures',
            },
        ),
        migrations.CreateModel(
            name='PortalUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=512, null=True)),
                ('password', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.portalgroups')),
            ],
            options={
                'db_table': 'portal_users',
            },
        ),
        migrations.CreateModel(
            name='Peoples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=512, null=True)),
                ('surname', models.CharField(blank=True, max_length=512, null=True)),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('name2', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.orgs')),
            ],
            options={
                'db_table': 'peoples',
            },
        ),
    ]