# Generated by Django 4.0.1 on 2022-01-28 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_tags_delete_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='categories',
            new_name='category',
        ),
    ]