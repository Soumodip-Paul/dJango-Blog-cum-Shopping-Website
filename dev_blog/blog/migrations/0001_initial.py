# Generated by Django 3.2.9 on 2021-11-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(max_length=50)),
                ('blog_content', models.TextField()),
                ('blog_author', models.CharField(max_length=50)),
                ('blog_image', models.ImageField(blank=True, default='', null=True, upload_to='shop/image')),
                ('blog_category', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]