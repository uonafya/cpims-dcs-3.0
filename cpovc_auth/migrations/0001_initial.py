# Generated by Django 4.2.16 on 2024-10-10 08:19

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.CharField(default='Public', max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True)),
                ('password_changed_timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='CPOVCPermission',
            fields=[
                ('permission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.permission')),
                ('permission_description', models.CharField(max_length=255)),
                ('permission_set', models.CharField(max_length=100)),
                ('permission_type', models.CharField(blank=True, max_length=50)),
                ('restricted_to_self', models.BooleanField(blank=True, default=False)),
                ('restricted_to_org_unit', models.BooleanField(blank=True, default=False)),
                ('restricted_to_geo', models.BooleanField(blank=True, default=False)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'auth_permission_detail',
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name='CPOVCProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(default='{}')),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'auth_user_profile',
            },
        ),
        migrations.CreateModel(
            name='CPOVCRole',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('group_id', models.CharField(max_length=5)),
                ('group_name', models.CharField(max_length=100)),
                ('group_description', models.CharField(max_length=255)),
                ('restricted_to_org_unit', models.BooleanField(blank=True, default=False)),
                ('restricted_to_geo', models.BooleanField(blank=True, default=False)),
                ('automatic', models.BooleanField(default=False)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'auth_group_detail',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='CPOVCUserRoleGeoOrg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'auth_user_groups_geo_org',
            },
        ),
    ]
