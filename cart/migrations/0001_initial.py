# Generated by Django 4.1.2 on 2022-12-01 15:12

import core.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0003_alter_category_managers_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='데이터가 생성된 일자입니다.', verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='데이터가 수정된 사용자입니다.', verbose_name='수정일')),
                ('is_deleted', models.BooleanField(blank=True, default=False, editable=False, help_text='데이터 삭제 여부입니다.', verbose_name='삭제 여부')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, help_text='데이터를 삭제한 일자입니다.', null=True, verbose_name='삭제일')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='수량')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_item', to='shop.item', verbose_name='상품')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='구매자')),
            ],
            options={
                'verbose_name': '장바구니',
                'verbose_name_plural': '장바구니',
                'db_table': 'cart_tb',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', core.managers.CustomModelManager()),
            ],
        ),
    ]
