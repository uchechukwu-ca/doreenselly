# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0006_auto_20161116_1004'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='ContactUs',
        ),
    ]
