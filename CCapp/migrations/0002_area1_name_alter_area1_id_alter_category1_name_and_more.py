# Generated by Django 5.1.2 on 2024-11-11 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CCapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area1',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='area1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category1',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='dm',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='supportdm',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='DefaultName', max_length=15, verbose_name='名前'),
        ),
    ]