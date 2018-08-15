from django.shortcuts import render
from django.db import connection
import datetime

def get_cursor():
    return connection.cursor()

def index(request):
    date = request.POST.get("date")
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if not date or date == '':
        sql1 = "SELECT note,JGMC,BTIEM,ETIEM,COMPLETE,taskid,levels FROM q" \
              "zj_etl_v21.sys_logtask A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
              "AND to_char(BTIEM,'yyyy-mm-dd') = '%s'" \
              "where (complete is null or complete = 2) and levels = 1 and B.used = 1" % today
        sql2 = "SELECT note,JGMC,BTIEM,ETIEM,COMPLETE,taskid,levels FROM q" \
               "zj_etl_v21.sys_logtask A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
               "AND to_char(BTIEM,'yyyy-mm-dd') = '%s'" \
               "where (complete is null or complete = 2) and levels = 2 and B.used = 1" % today
    else:
        sql1 = "SELECT note,JGMC,BTIEM,ETIEM,COMPLETE,taskid,levels FROM q" \
              "zj_etl_v21.sys_logtask A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
              "AND to_char(BTIEM,'yyyy-mm-dd') = '%s'" \
              "where (complete is null or complete = 2) and levels = 1 and B.used = 1" % date
        sql2 = "SELECT note,JGMC,BTIEM,ETIEM,COMPLETE,taskid,levels FROM q" \
               "zj_etl_v21.sys_logtask A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
               "AND to_char(BTIEM,'yyyy-mm-dd') = '%s'" \
               "where (complete is null or complete = 2) and levels = 2 and B.used = 1" % date
    cursor1 = get_cursor()
    cursor2 = get_cursor()
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    messages1 = cursor1.fetchall
    messages2 = cursor2.fetchall
    return render(request, 'info.html', context={'messages1': messages1, 'messages2': messages2,
                                                  'date': date, 'today': today})

def info_Error(request):
    info_id = request.GET.get('id')
    sql = "select a.runno,a.prclognote,a.objnote,a.ctiem,a.prcsql " \
              "from qzj_etl_v21.sys_logprc a " \
              "where error='1' and a.objnote !='N/A' and a.taskid='%s' " \
              "order by a.runno;" % info_id
    cursor = get_cursor()
    cursor.execute(sql)
    messages = cursor.fetchall
    return render(request, 'info_Error.html', context={'messages': messages})

def info_Doing(request):
    info_id = request.GET.get('id')
    note = request.GET.get('note')
    if note == "[2100 接入数据发送翻库]":
        sql = "select a.runno,a.prclognote,a.objnote,sum(a.records) as records " \
              "from qzj_etl_v21.sys_logprc a " \
              "where a.objnote != 'N/A' and a.prclogname in('P_DbTran_JrqBak','P_DbTran_JrqClear','P_DbTran_JrqToFsq') " \
              "and a.taskid='%s' " \
              "group by a.runno,a.prclognote,a.objnote order by a.runno;" % info_id
    else:
        sql = "select a.runno,a.prclognote,a.objnote,sum(a.records) as records " \
              "from qzj_etl_v21.sys_logprc a " \
              "where a.objnote != 'N/A' and pid='ALL' and a.taskid='%s'" \
              "group by a.runno,a.prclognote,a.objnote order by a.runno;" % info_id
    cursor = get_cursor()
    cursor.execute(sql)
    messages = cursor.fetchall
    return render(request, 'info_Doing.html', context={'messages': messages})