# Generated by Django 4.1.2 on 2022-10-27 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='best_item',
            field=models.BooleanField(db_index=True, default=False, verbose_name='베스트 아이템'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(verbose_name='리뷰'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]