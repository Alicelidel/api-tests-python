#! usr/bin/python3
# -*- coding: utf-8 -*-
import pyodbc

server = 'server_ip'
database = 'db-name'
username = 'user'
password = 'password'
driver = '{SQL Server}' # Driver you need to connect to the database
port = '1433'
cnn = pyodbc.connect('DRIVER='+driver+';PORT=port;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+
                 ';PWD='+password)
cursor = cnn.cursor()

