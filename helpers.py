#! usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import pyodbc
import datetime


server = 'server_ip'
database = 'db_name'
username = 'user'
password = 'password'
driver = '{SQL Server}'  # Driver you need to connect to the database
port = '1433'
params = server, database, \
    username, password, \
    driver, port
string =  r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'
result1 = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'
result2 = r' and smth more'
result3 = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'
result4 = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'
result = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'



def get_max_id(params):
    server, database, username, password, driver, port = params

    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnn.cursor()
    cursor.execute("select MAX(id) from db.table")

    max_id = cursor.fetchone()
    if max_id[0] is None:
        max_id = 1
    else:
        max_id = int(max_id[0]) + 1
    return max_id


def get_id(params):
    #next user will have this number
    server, database, username, password, driver, port = params

    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnn.cursor()
    cursor.execute('select MAX(id) from db.table')

    user_id = cursor.fetchone()
    if user_id[0] is None:
        user_id = 1
    else:
        user_id = int(user_id[0]) + 1
    return user_id



curr_id = get_id(params=params)
lgn = 'TestUser{}'.format(curr_id)
psw = '1'
max_id = get_id(params=params)

get_login = curr_id, lgn, psw, max_id


def slowness(curr_id, max_id):
    atm = datetime.datetime.now()
    max_id1 = max_id
    max_id2 = max_id + 1
    print('Maximum user id -', curr_id, '; two biggest ids from table -', max_id1, max_id2)
    # creating user
    seq = [string, str(curr_id)]
    result_string = ' '.join(seq)
    try:
        stat, _ = subprocess.getstatusoutput(result_string)
        print('make user ', stat)
    except:
        print('Exception caught.')
        stat = '1'
    intheend = datetime.datetime.now() - atm
    print(intheend)
    return stat


def set_state(max_id):
    #connection to BD
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnn.cursor()
    #finding task for the target
    cursor.execute("select ID from db.table where id={};".format(max_id))
    task_id = cursor.fetchone()
    task_id = task_id[0]
    print('task id is ', task_id)

    result1 = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth with '
    result2 = r' and do smth else'
    seq = [result1, str(max_id), result2]
    job_string1 = ''.join(seq)
    try:
        stat1, _ = subprocess.getstatusoutput(job_string1)
        print('upload target', stat1)
    except:
        print('Another exception caught')
        stat1 = '1'
    result3 = r'psexec \\server_ip -u Administrator -p Password -nobanner do smth'
    seq = [result3, str(max_id)]
    job_string2 = ''.join(seq)
    try:
        stat2, _ = subprocess.getstatusoutput(job_string2)
        print('change to 2', stat2)
    except:
        print('Another exception on 2')
    while True:
        cursor.execute('select state from db.table where id=[];'.format(max_id))
        state = cursor.fetchone()
        print('state - ', state[0])
        if state[0] == 4:
            print('state - ', state[0])
            break
    cursor.execute('exec tasks.task @task={};'.format(task_id))
    cnn.commit()
    while True:
        cursor.execute('select state from db.table where id={};'.format(max_id))
        state = cursor.fetchone()
        print('state - ', state[0])
        if state[0] == 6:
            print('state - ', state[0])
            break
    cursor.execute('exec tasks.task @task={};'.format(task_id))
    cnn.commit()
    while True:
        cursor.execute('select state from db.table where id={};'.format(max_id))
        state = cursor.fetchone()
        print('state - ', state[0])
        if state[0] == 9:
            print('state - ', state[0])
            break

    cnn.close()

    return True