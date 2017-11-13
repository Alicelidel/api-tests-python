#! usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
from .st import user,password


def search_connection(user, password, params):
    try:
        url = 'http://address/smth1'
        r = requests.get(url, auth=HTTPBasicAuth(user, password), params=params)
        response = r.status_code, r.text
    except Exception as e:
        #if no response, return error
        response = e
    finally:
        return response


def search_connection_post(user, password, params):
    try:
        url = 'http://address/smth1'
        headers = {'user-agent': '0'}
        r = requests.post(url, auth=HTTPBasicAuth(user, password), params=params, headers=headers)
        response = r.status_code, r.text
    except Exception as e:
        #if no response, return error
        response = e
    finally:
        return response


def max_connection(user, password, params):
    try:
        url = 'http://address/smth2'
        r = requests.get(url, auth=HTTPBasicAuth(user, password), params=params)
        response = r.status_code
    except Exception as e:
        #if no response, return error
        response = e
    finally:
        return response


def export_connection(user, password, params):
    try:
        url = 'http://address/smth3'
        r = requests.get(url, auth=HTTPBasicAuth(user, password), params=params)
        response = r.status_code
    except Exception as e:
        #returns error if no response
        response = e
    finally:
        return response


def conn_to_adm(user, password):
    try:
        url = 'http://address/admin'
        r = requests.get(url, auth=HTTPBasicAuth(user, password), params=params)
        response = r.status_code
    except Exception as e:
        #returns error if no response
        response = e
    finally:
        return response


def main():
    params = {'param': 'param'}
    search_resp = search_connection(user, password, params)
    print(search_resp)

    params = {'id': '1'}
    max_resp = max_connection(user, password, params)
    print(max_resp)

    scan_resp = export_connection(user, password, params)
    print(scan_resp)

if __name__ == "__main__":
    main()