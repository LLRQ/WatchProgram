from django.shortcuts import render
from django.db import connection

def get_cursor():
    return connection.cursor()

def dictfetchall(cursor):
    # "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def index(request):
    sql = "select B.pid,jgmc,levels,nvl(status,0) status " \
          "from (select distinct pid,1 status from qzj_etl_v21.tb_tablespace_monitor " \
          "where rate_used_max > 90) A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid"
    cursor = get_cursor()
    cursor.execute(sql)
    messages = dictfetchall(cursor)

    return render(request, 'space.html', context={'messages': messages})

def detail(request):
    info_id = request.GET.get('id')
    sql = "select * from qzj_etl_v21.tb_tablespace_monitor where pid = '%s' order by RATE_USED_MAX desc" % info_id
    cursor = get_cursor()
    cursor.execute(sql)
    messages = cursor.fetchall

    return render(request, 'space_detail.html', context={'messages': messages})
