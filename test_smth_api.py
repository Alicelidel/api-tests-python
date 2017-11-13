#! usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
import subprocess
from .helpers import get_login, slowness, set_state
from .smth_api import search_connection, export_connection, max_connection, search_connection_post, conn_to_adm
from .settings import string, result


def setup():
    print('\nset up test')


def teardown():
    print('\ntear down test')


@pytest.mark.slow
def test_slowness():
    curr_id, _, _, max_id = get_login
    code = slowness(curr_id, max_id)
    max_id1 = max_id
    max_id2 = max_id + 1
    max1 = set_state(max_id1)
    max2 = set_state(max_id2)
    assert code == 0
    assert max1 is True
    assert max2 is True


def test_search_has_result_author():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    author = 'Author{}'.format(curr_id)
    params = {'authors': author}
    status, result = search_connection(login, passw, params)
    assert author in result
    assert status == 200

def test_search_has_result_author_main_number():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    author = 'Author{}'.format(curr_id)
    main_number = 'MainNum{}'.format(curr_id)
    params = {'authors': author, 'main_number': main_number}
    status, result = search_connection(login, passw, params)
    assert author in result
    assert main_number in result
    assert status == 200

def test_search_has_result_author_title():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    author = 'Author{}'.format(curr_id)
    title = 'Title{}'.format(curr_id)
    params = {'authors': author, 'title': title}
    status, result = search_connection(login, passw, params)
    assert author in result
    assert title in result
    assert status == 200


def test_search_has_result_text():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    text = 'VEcordia'
    params = {'search_region': '2', 'ftss_request': text}
    status, result = search_connection(login, passw, params)
    assert status == 200

def test_search_has_result_main_number():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    main_number = 'MainNum{}'.format(curr_id)
    params = {'main_number': main_number}
    status, result = search_connection(login, passw, params)
    assert main_number in result
    assert status == 200


def test_search_has_result_title():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    title = 'Title{}'.format(curr_id)
    params = {'title': title}
    status, result = search_connection(login, passw, params)
    assert title in result
    assert status == 200


def test_search_no_result_plain():
    #asquire id, login and pass for the test
    _, login, passw, _ = get_login
    print(get_login)
    #plain request
    params = {}
    status, result = search_connection(login, passw, params)
    assert status == 400


def test_search_no_result_sql():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    #try to pass sql-expression to serach
    params = "select * from lbr.LB_DOCUMENTS where TITLE=Title{}".format(curr_id)
    status, result = search_connection(login, passw, params)
    assert status == 400

@pytest.mark.xfail
def test_search_has_result_post():
    #asquire id, login and pass for the test
    curr_id, login, passw, _ = get_login
    print(get_login)
    author = 'Author{}'.format(curr_id)
    params = {'authors': author}
    status, result = search_connection_post(login, passw, params)
    assert author in result
    assert status == 200


def test_unexsist_url():
    curr_id, login, passw, _ = get_login
    print(get_login)
    params = 'iamunexsist'
    status, result = search_connection(login, passw, params)
    assert status == 400


def test_search_no_result():
    curr_id, login, passw, _ = get_login
    #user has access to only one target, therefore there should not be any result
    author = 'Author{}'.format(curr_id - 1)
    params = {'authors': author}
    status, result = search_connection(login, passw, params)
    assert author not in result
    assert status == 200


@pytest.mark.parametrize('logpass', [('TestUserr', '1'), ('testuser', '1'),
                                     ('Testuser', '1'), ('testUser', '1'),
                                     ('tested', '111')])
def test_search_unauthorised(logpass):
    curr_id, _, _, _ =get_login
    #search for book with not-existing user
    login, passw = logpass
    author = 'Author{}'.format(curr_id - 1)
    params = {'authors': author}
    status, result = search_connection(login, passw, params)
    assert status == 401


def test_export_has_access():
    _, login, passw, max_id = get_login
    params = {'id': max_id, 'pages': '1'}
    status = export_connection(login, passw, params)
    #return code should be not 401, but 200
    assert status == 200

def test_export_has_access_plain():
    _, login, passw, max_id = get_login
    params = {}
    status = export_connection(login, passw, params)
    #return code not found
    assert status == 400

def test_export2_no_access():
    _, _, _, max_id = get_login
    params = {'id': max_id, 'pages': '1'}
    login, passw = 'noname', '1'
    status  = export_connection(login, passw, params)
    #return code should not be '200'
    assert status != 200

@pytest.mark.parametrize('formats',
                         ['1', '2', '3', '4'])
def test_export_max_has_access(formats):
    _, login, passw, max_id = get_login
    params = {'id': max_id, 'pages': '1', 'format': formats}
    status = max_connection(login, passw, params)
    #return code currently - internal server error
    assert status == 200

def test_export_max_has_access_plain():
    _, login, passw, max_id = get_login
    params = {}
    status = max_connection(login, passw, params)
    #return code currently - internal server error
    assert status == 400

def test_export_max_no_access():
    _, _, _, max_id = get_login
    params = {'id': max_id, 'pages': '1'}
    login, passw = 'noname', '1'
    #return code should be unauthorised
    status = max_connection(login, passw, params)
    assert status != 200


def test_search_two_maxs():
    # test whether both books are in result
    curr_id, login, passw, _ = get_login
    author1 = 'Author{}'.format(curr_id)
    author2 = 'Author{}{}'.format(curr_id, curr_id)
    search = '{}, {}'.format(author1, author2)
    params = {'authors': search}
    status, result = search_connection(login, passw, params)
    assert author1, author2 in result
    assert status == 200


def test_search_two_maxs_two_requests():
    curr_id, login, passw, _ = get_login
    author1 = 'Author{}'.format(curr_id)
    author2 = 'Author{}1'.format(curr_id)
    search = '{}'.format(author1)
    params = {'authors': search, 'nrows': '1', 'from': '1'}
    status1, result1 = search_connection(login, passw, params)
    params = {'authors': search, 'nrows': '1', 'from': '2'}
    status2, result2 = search_connection(login, passw, params)
    assert status1 == 200
    assert status2 == 200
    assert author1 in result1
    assert author2 in result2


def test_default_admin():
    user, password = 'admin', '1'
    res = conn_to_adm(user, password)
    assert res == 404


def main():
    curr_id, _, _, max_id = get_login
    seq = [string, curr_id]
    result_string = ' '.join(seq)
    try:
        #creating user
        stat, _ = subprocess.getstatusoutput(result_string)
        print(stat)
    except:
        print('Exception caught')
    seq = [result, max_id]
    job_string1 = ' '.join(seq)
    max_id += 1
    seq = [result, max_id]
    job_string2 = ' '.join(seq)
    try:
        stat2, _ = subprocess.getstatusoutput(job_string1)
        stat3, _ = subprocess.getstatusoutput(job_string2)
        print(stat2)
        print(stat3)
    except:
        print('Another exception caught')


if __name__ == "__main__":
    args_str = "-v -l -x --color(yes)  --tb=long"
    pytest.main(args_str.split(" "))