# Generated by Django 4.2.9 on 2024-07-24 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_alter_networknode_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="networknode",
            options={
                "ordering": ("title", "type"),
                "verbose_name": "Сетевое звено",
                "verbose_name_plural": "Сетевые звенья",
            },
        ),
    ]
