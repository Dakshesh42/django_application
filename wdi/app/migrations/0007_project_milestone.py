# Generated by Django 4.1.5 on 2023-03-22 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_menu_alter_employee_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="milestone",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
