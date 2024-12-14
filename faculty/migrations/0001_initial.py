# Generated by Django 5.1.4 on 2024-12-14 16:15

import django.db.models.deletion
import django.utils.timezone
import faculty.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('abstract', models.CharField(max_length=500)),
                ('keywords', models.JSONField(default=list)),
                ('publisher', models.CharField(blank=True, max_length=75, null=True)),
                ('publish_date', models.DateField()),
                ('pdf', models.FileField(blank=True, null=True, upload_to='uploads/pdfs/')),
                ('pages', models.CharField(blank=True, max_length=30, null=True)),
                ('category', models.CharField(editable=False, max_length=15)),
                ('views', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('abbreviation', models.CharField(max_length=5, unique=True)),
                ('publication_count', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fid', models.CharField(editable=False, max_length=25, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('name', models.CharField(max_length=75)),
                ('designation', models.CharField(choices=[('P', 'Professor'), ('ASP', 'Assistant Professor'), ('AP', 'Associate Professor'), ('RS', 'Research Scholar'), ('S', 'Student')], default='AP', max_length=5)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superAdmin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.department')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', faculty.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='faculty.publication')),
                ('content', models.TextField(blank=True, null=True)),
                ('volume', models.IntegerField(default=1)),
                ('impact_factor', models.FloatField(default=0.0)),
                ('h_index', models.IntegerField(default=0)),
            ],
            bases=('faculty.publication',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='faculty.publication')),
                ('edition', models.IntegerField(default=1)),
                ('language', models.CharField(choices=[('Eng', 'English'), ('Hin', 'Hindi'), ('Asm', 'Assamese')], default='Eng', max_length=10)),
                ('isbn', models.CharField(blank=True, max_length=20, null=True)),
                ('issn', models.CharField(blank=True, max_length=20, null=True)),
            ],
            bases=('faculty.publication',),
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cited_by', to='faculty.publication')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citing_publication', to='faculty.publication')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.BigIntegerField(default=1234567890)),
                ('profile_img', models.ImageField(blank=True, default='user_profile/profile_default.png', upload_to='user_profile')),
                ('qualification', models.CharField(blank=True, max_length=255, null=True)),
                ('co_authors', models.JSONField(blank=True, null=True)),
                ('citation_count', models.IntegerField(default=0)),
                ('h_index', models.IntegerField(default=0)),
                ('h5_median', models.IntegerField(default=0)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]