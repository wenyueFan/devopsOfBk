# -*- coding: utf-8 -*-

from common.log import logger
from common.mymako import render_mako_context, render_json

from account.decorators import login_exempt
from iwork.models import workRecord


def home(request):
    """
    Home Page
    """
    return render_mako_context(request, '/iwork/home.html')


def save_record(request):
    """
    保存会议数据
    """
    theme = request.POST.get('theme', '')
    content = request.POST.get('content', '')

    data = {
        'theme': theme,
        'content': content,
        'username': request.user.username,
    }
    result = workRecord.objects.save_record(data)

    return render_json(result)


def records(request):
    """
    查询会议记录
    """
    record_list = workRecord.objects.all().order_by('-id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'index': index,
            'theme': record.theme,
            'content': record.content,
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})