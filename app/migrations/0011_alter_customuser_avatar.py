# Generated by Django 4.2.7 on 2024-05-16 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_post_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='images/Blog-post/post_covers/default.png', null=True, upload_to=''),
        ),
    ]
