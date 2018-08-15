from django.shortcuts import render
from django.db import connection
from threading import Thread
import subprocess
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

def ping(request):
    sql = "select jgmc,ip_address,db_port,levels from qzj_etl_v21.TB_JGPID_ALL where used = 1"
    cursor = get_cursor()
    cursor.execute(sql)
    global messages
    messages = dictfetchall(cursor)
    # messages[54] = {'JGMC': 'test', 'IP_ADDRESS': '193.168.103.123'},{'JGMC': '宝山', 'IP_ADDRESS': '172.16.116.3'}
    # messages = [{'JGMC': 'test', 'IP_ADDRESS': '193.168.103.123'}, {'JGMC': '宝山', 'IP_ADDRESS': '172.16.116.3'}]
    # print(messages, len(messages))
    threadnum = len(messages)
    th_lst = []  # 存放线程
    for i in range(threadnum):
        ip = messages[i]['IP_ADDRESS']
        port = messages[i]['DB_PORT']
        th = Thread(target=pingme, args=(i, ip, port))
        th_lst.append(th)
        th = Thread(target=pingmeplus, args=(i, ip, 22))
        th_lst.append(th)

    for th in th_lst:  # 开始所有线程
        th.start()

    for th in th_lst:  # 结束所有已完成线程
        th.join()
    return render(request, 'ping.html', context={'messages': messages})

def pingme(i, ip, port):
    flag = 0
    for a in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((ip, int(port)))
            # messages[i]['IP_ADDRESS'] = '通畅'
        except Exception:
            flag += 1
            # print('%s失败第%d次' % (ip, flag))
            # messages[i]['IP_ADDRESS'] = '失败'
        sock.close()
    # print('%s成功了%d次' % (ip, 3 - flag))
    if flag == 3:
        messages[i]['IP_ADDRESS'] = '失败'
    else:
        messages[i]['IP_ADDRESS'] = '通畅'

    # sock.bind((ip, int(port)))  # 配置soket，绑定IP地址和端口号
    # sock.listen(5)  # 设置最大允许连接数，各连接和server的通信遵循FIFO原则
    # connection, address = sock.accept()
    # buf = connection.recv(1024)
    # print('**********', buf)
    # if buf == 1:
    #     messages[i]['IP_ADDRESS'] = '通畅'
    # elif buf == 0:
    #     messages[i]['IP_ADDRESS'] = '失败'
    # ret = subprocess.call('ping %s' % ip, shell=True, stderr=subprocess.STDOUT)
    # if ret == 0:
    #     messages[i]['IP_ADDRESS'] = '可以Ping通'
    # elif ret == 1:
    #     messages[i]['IP_ADDRESS'] = 'Ping失败'

def pingmeplus(i, ip, port):
    flag = 0
    for a in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((ip, int(port)))
            # messages[i]['IP_ADDRESS'] = '通畅'
        except Exception:
            flag += 1
            # print('%s失败第%d次' % (ip, flag))
            # messages[i]['IP_ADDRESS'] = '失败'
        sock.close()
    # print('%s成功了%d次' % (ip, 3 - flag))
    if flag == 3:
        messages[i]['DB_PORT'] = '失败'
    else:
        messages[i]['DB_PORT'] = '通畅'


