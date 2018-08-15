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
    sql = "SELECT jgmc,levels,filesystem,k_blocks,A.used,available,rate_used,mounted_on FROM " \
          "qzj_etl_v21.tb_diskspace A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
          "order by jgmc, rate_used desc"
    cursor = get_cursor()
    cursor.execute(sql)
    messages = dictfetchall(cursor)
    return render(request, 'disc.html', context={'messages': messages})

