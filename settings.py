#! usr/bin/python3
# -*- coding: utf-8 -*-

server = 'server_ip'
database = 'db_name'
username = 'user'
password = 'password'
driver = '{SQL Server}'  # Driver you need to connect to the database
port = '1433'

params = server, database, \
    username, password, \
    driver, port

string =  r'psexec \\server_ip do smth'
result = r'psexec \\server_ip do smth'


