from django.shortcuts import render
from django.db import connection
import datetime
from threading import Thread
import socket


def get_cursor():
    return connection.cursor()

def dictfetchall(cursor):
    # "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def home(request):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    sql1 = "SELECT BTIEM,COMPLETE FROM q" \
           "zj_etl_v21.sys_logtask A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
           "AND to_char(BTIEM,'yyyy-mm-dd') = '%s'" \
           "where (complete is null or complete = 2) and B.used = 1" % today
    sql2 = "select jgmc,ip_address,db_port,levels from qzj_etl_v21.TB_JGPID_ALL where used = 1"
    sql3 = "select pid from qzj_etl_v21.tb_tablespace_monitor where rate_used_max > 90"
    sql4 = "SELECT jgmc,levels,filesystem,k_blocks,A.used,available,rate_used,mounted_on FROM " \
           "qzj_etl_v21.tb_diskspace A right join qzj_etl_v21.TB_JGPID_ALL B on A.pid = B.pid " \
           "order by jgmc, rate_used desc"
    cursor1 = get_cursor()
    cursor2 = get_cursor()
    cursor3 = get_cursor()
    cursor4 = get_cursor()
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)

    messages1 = dictfetchall(cursor1)
    if not messages1 or messages1 == '':
        flag1 = True
    else:
        flag1 = False

    messages2 = dictfetchall(cursor2)
    global flag2
    flag2 = []
    flag2.append(True)
    threadnum = len(messages2)
    th_lst = []  # 存放线程
    for i in range(threadnum):
        ip = messages2[i]['IP_ADDRESS']
        port = messages2[i]['DB_PORT']
        th = Thread(target=pingme, args=(ip, port))
        th_lst.append(th)
        th = Thread(target=pingmeplus, args=(ip, 22))
        th_lst.append(th)

    for th in th_lst:  # 开始所有线程
        th.start()

    for th in th_lst:  # 结束所有已完成线程
        th.join()


    messages3 = dictfetchall(cursor3)
    if not messages3 or messages3 == '':
        flag3 = True
    else:
        flag3 = False


    messages4 = dictfetchall(cursor4)
    flag4 = True
    print(messages4)
    for ob in messages4:
        if ob['RATE_USED'] > '90':
            flag4 = False
            break

    return render(request, 'Home.html', context={'flag1': flag1, 'flag2': flag2[0], 'flag3': flag3, 'flag4': flag4})

def pingme(ip, port):
    flag = 0
    for a in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((ip, int(port)))
        except Exception:
            flag += 1
        sock.close()
    if flag == 3:
        flag2[0] = False


def pingmeplus(ip, port):
    flag = 0
    for a in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((ip, int(port)))
        except Exception:
            flag += 1
        sock.close()
    if flag == 3:
        flag2[0] = False
