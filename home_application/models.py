# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import datetime
from django.db import models


class dbExchangeLogManager(models.Manager):
    def save_record(self, data):
        """
        保存数据库切换记录
        """
        try:
            dbExchangeLog.objects.create(
                main_ip=data.get('main_ip'),
                stadnby_ip=data.get('stadnby_ip'),
                exchange_direction=data.get('exchange_direction'),
                operator=data.get('operator'),
                create_time=data.get('create_time'),
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class dbExchangeLog(models.Model):
    """
    db切换记录
    """
    main_ip = models.CharField(u"主库ip", max_length=15)
    stadnby_ip = models.CharField(u"备库ip", max_length=15)
    exchange_direction = models.CharField(u"切换方向", max_length=15)
    create_time = models.DateTimeField(u"切换时间", default=datetime.datetime.now())
    operator = models.CharField(u"记录人", max_length=64)
    objects = dbExchangeLogManager()

    def __unicode__(self):
        return self.theme

    class Meta:
        verbose_name = u"数据库切换记录"
        verbose_name_plural = u"数据库切换记录"

class RackManager(models.Manager):
    def save_record(self, data):
        """
        保存机柜记录
        """
        try:
            Rack.objects.create(
                name=data.get('name'),
                height=data.get('height'),
                row_num=data.get('row_num'),
                column_num=data.get('column_num'),
                machine_room=data.get('machine_room'),
                operator=data.get('operator')
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result

class Rack(models.Model):
    """
    机柜
    """
    name = models.CharField(u"机柜名称", max_length=15,unique=True)
    height = models.CharField(u"机柜高度", max_length=2)
    row_num = models.CharField(u"所在行", max_length=2)
    column_num = models.CharField(u"所在列", max_length=2)
    machine_room = models.CharField(u"所在机房", max_length=2)
    create_time = models.DateTimeField(u"创建时间", default=datetime.datetime.now())
    operator = models.CharField(u"记录人", max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"机柜"
        verbose_name_plural = u"机柜"

