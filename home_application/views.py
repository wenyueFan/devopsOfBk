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

from models import dbExchangeLog
from models import Rack
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request

def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/show_Computer_room.html')


def dbexchangelog(request):
    """

    """
    return render_mako_context(request, '/home_application/dbexchangelog.html')
def new_dbexchangelog(request):
    """

    """
    return render_mako_context(request, '/home_application/new_dbexchangelog.html')

def getDbExchangeLog(request):
    record_list = dbExchangeLog.objects.all().order_by('-id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'index': index,
            'main_ip': record.main_ip,
            'stadnby_ip': record.stadnby_ip,
            'exchange_direction': record.exchange_direction,
            'operator': record.operator,
            #'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})
def newDbExchangeLog(request):
    """
    跳转至新增界面
    """
    return render_mako_context(request, '/home_application/new_dbexchangelog.html')
def save_DbExchangeLog(request):
    """
    调用作业平台执行主备切换，如成功保存数据
    """
    main_ip = request.POST.get('main_ip', '')
    stadnby_ip = request.POST.get('stadnby_ip', '')
    exchange_direction = request.POST.get('exchange_direction', '')
    operator = request.POST.get('operator', '')
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': "7","bk_job_id": "24",
              "steps": [{
                  "script_timeout": 1000,
                  "ip_list": [
                      {
                          "bk_cloud_id": 0,
                          "ip": main_ip
                      }
                  ],
                  "account": "rootbk",
                  "step_id": 46
              }]
              }
    resp = client.job.execute_job(**kwargs)

    if resp.get('result'):
        data = resp.get('data', [])
        job_instance_id = data.get("job_instance_id")
        #message = resp.get('message')

        data = {"main_ip":main_ip,
                "stadnby_ip": stadnby_ip,
                "exchange_direction": exchange_direction,
                "operator": operator}
        dbExchangeLog.objects.save_record(data)
        data.message=job_instance_id
        #print resp.get('result')
        result = {'result': resp.get('result'), 'data': data}
    return render_json(result)

def updateJf2dRptData(request):
    """
    调用作业平台执行更新机房展示数据
    """
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': "7","bk_job_id": "29"}
    resp = client.job.execute_job(**kwargs)

    if resp.get('result'):
        data = resp.get('data', [])
        result = {'result': resp.get('result'), 'data': data}
    return render_json(result)

def search_instFromBK(request):
    """
    查询实例
    """
    jfid = request.POST.get('jfid', '')
    client = get_client_by_request(request)
    kwargs = {"bk_supplier_account" :0,
              "bk_obj_id" : "jskj_rpt_jf2d",
                "condition":{
                    "jskj_rpt_jf2d":[
                        {
                            "field":"jfmc",
                            "operator":"$eq",
                            "value":jfid
                        }
                    ]
                }
              }
    resp = client.cc.search_inst(**kwargs)

    result = {'result': resp}
    return render_json(result)
def showComputerRoom(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/show_Computer_room.html')

def link2RackManageUrl(request):
    """
    机位管理
    """
    return render_mako_context(request, '/home_application/rackManage.html')

def getRackList(request):
    record_list = Rack.objects.all().order_by('-id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'index': index,
            'id': record.id,
            'name': record.name,
            'height': record.height,
            'row_num': record.row_num,
            'column_num': record.column_num,
            'machine_room': record.machine_room,
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})

def save_Rack(request):
    name = request.POST.get('name', '')
    height = request.POST.get('height', '')
    row_num = request.POST.get('row_num', '')
    column_num = request.POST.get('column_num', '')
    machine_room = request.POST.get('machine_room', '')
    operator = request.user.username
    data = {"name": name,
            "height": height,
            "row_num": row_num,
            "column_num": column_num,
            "machine_room": machine_room,
            "operator": operator}
    result = Rack.objects.save_record(data)
    return render_json(result)

def newRack(request):
    """
    进入新建机位界面
    """
    return render_mako_context(request, '/home_application/new_rack.html')

def deleteRack(request):
    """
    删除机柜
    """
    rackName = request.POST.get("rackName", '')
    try:
        Rack.objects.filter(name = rackName).delete()
        result = {'result': True, 'message': u"删除成功"}
    except Exception, e:
        result = {'result': False, 'message': u"删除失败, %s" % e}
    return render_json(result)

def getRackByRowNum(request):
    """
    根据所在行拿到机柜,并升序排列
    """
    rowNum = request.POST.get("rowNum", '')
    try:
        data = Rack.objects.filter(row_num = rowNum).order_by('column_num')

        tempdata = []
        for index, record in enumerate(data):
            tempdata.append({
                'name': record.name,
                'height': record.height,
                'row_num': record.row_num,
                'column_num': record.column_num,
            })
        result = {'result': True, 'message': u"获取成功", 'data': tempdata}
    except Exception, e:
        result = {'result': False, 'message': u"获取失败, %s" % e}
    return render_json(result)
