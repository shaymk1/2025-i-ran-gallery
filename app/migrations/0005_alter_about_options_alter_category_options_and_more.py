# Generated by Django 5.2 on 2025-04-07 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_blog_options_blog_categories_blog_last_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='about',
            options={'verbose_name_plural': 'About Us'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Photos'},
        ),
    ]
