# Generated by Django 5.1.3 on 2025-02-15 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_rename_content_testimony_content_ar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', max_length=1200, upload_to='blog/', verbose_name='Blog Image')),
                ('title_fr', models.CharField(max_length=200)),
                ('title_ar', models.CharField(max_length=200)),
                ('content_fr', models.TextField()),
                ('content_ar', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Blogs',
                'ordering': ['-created_at'],
            },
        ),
    ]
