# Generated by Django 4.1.2 on 2022-12-10 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_category_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_category', to='shop.category', verbose_name='상위 카테고리'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_category', to='shop.category', verbose_name='카테고리'),
        ),
        migrations.DeleteModel(
            name='CategoryDetail',
        ),
    ]
