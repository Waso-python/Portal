# Generated by Django 4.0.2 on 2022-07-12 10:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IndexpageOrder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('num_proc', models.CharField(max_length=10)),
                ('link_proc', models.CharField(max_length=500)),
                ('partner', models.CharField(max_length=512)),
                ('summ_proc', models.IntegerField()),
                ('count_order', models.IntegerField()),
                ('subj_proc', models.CharField(max_length=512)),
                ('actual_for_me', models.IntegerField()),
                ('add_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'indexpage_order',
                'managed': False,
            },
        ),
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
            name='RawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_proc', models.CharField(max_length=128)),
                ('link_proc', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=128)),
                ('type_proc', models.CharField(max_length=128)),
                ('partner', models.CharField(max_length=512)),
                ('partner_inn', models.CharField(max_length=512)),
                ('summ_proc', models.CharField(max_length=20)),
                ('count_order', models.CharField(max_length=5)),
                ('region', models.CharField(max_length=128)),
                ('law_proc', models.CharField(max_length=128)),
                ('subj_proc', models.CharField(max_length=512)),
                ('complete', models.IntegerField(default=0)),
                ('start_date', models.CharField(max_length=50)),
                ('end_date', models.CharField(max_length=50)),
                ('proc_comment', models.CharField(max_length=256)),
                ('inserted_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'raw_table',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
            ],
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
                ('link', models.CharField(max_length=521)),
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
                ('proc_number', models.CharField(max_length=512)),
                ('subject', models.CharField(blank=True, max_length=512, null=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('date_proc', models.DateTimeField(blank=True, null=True)),
                ('link', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deal_count', models.IntegerField()),
                ('law', models.ForeignKey(db_column='law', on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.laws')),
                ('orgs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.orgs')),
                ('places', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.marketplaces')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='indexpage.region')),
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
