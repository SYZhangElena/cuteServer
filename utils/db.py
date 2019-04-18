# conding = utf-8

import sqlite3
from sqlite3 import Error
import logging
import traceback
from io import StringIO
import os

#from settings import settings

#config = settings['config']
#DATABASE = config.get('sqlite', 'MATRIX_DB_FILE').strip('""')

DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATABASE = os.path.join(DIR, 'DB.db')

def trace(f):
    def _trace(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
        except:
            fp = StringIO()
            traceback.print_exc(file=fp)
            logging.exception(fp.getvalue())
            res = None
        return res
    return _trace


class ConnectionSingleton(object):
    conn = None

    def __new__(cls, **kwargs):
        print(kwargs)
        cls.database = kwargs.get('database', DATABASE)
        if cls.conn is None:
            cls.conn = sqlite3.connect(cls.database)
        return cls.conn


@trace
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = ConnectionSingleton(database=DATABASE)
        return conn
    except Error as e:
        logging.error(e)
    return None


@trace
def get_passwd_by_username(username):
    conn = create_connection(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT passwd FROM user WHERE username=?", (username,))
        row = cur.fetchone()
    logging.info(row)
    if not row:
        return None
    else:
        return row[0]


@trace
def insert_user(username, passwd):
    conn = create_connection(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username=?", (username,))
        t = cur.fetchone()
        if t:
            return None
        cur.execute("INSERT INTO user (username, passwd) VALUES (?, ?)", (username, passwd,))
    return cur.lastrowid


@trace
def get_user_list():
    conn = create_connection(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
    res = []
    for row in rows:
        if row:
            print(row)
            res.append((row[0], row[1]))
    return res

@trace
def insert_event(params):
    # 参数检测
    conn = create_connection(DATABASE)
    print(params)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO event VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?)", 
                (None, 
                params['createUserId'], params['helpUserId'], 
                params['isEnd'], params['createTime'],
                params['helpTime'], params['type'], 
                params['receiveName'], params['receivePhone'], 
                params['expressFirm'], params['getAddress'], 
                params['getTime'], params['note'], 
                params['tip'], params['sendAddress1'], 
                params['sendAddress2'],)
            )
        return True
    except Exception as why:
        logging.warning(why)
        return False

@trace
def change_event(params_list):
    """
    params: [{
        'event_id': value,
        'field': key,
        'value': value
    }]
    """
    # 参数检测
    conn = create_connection(DATABASE)
    print(params_list)
    success = True
    for params in params_list:
        event_id = params['event_id']
        field = params['field']
        value = params['value']
        try:
            with conn:
                cur = conn.cursor()
                cur.execute("UPDATE event SET {}=? WHERE id=?".format(field), 
                    (value, event_id),
                )
        except Exception as why:
            logging.warning(why)
            success = False
            break
    return success

@trace
def get_event_list():
    conn = create_connection(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM event WHERE isEnd=0 ORDER BY createTime DESC")
        rows = cur.fetchall()
    res = []
    for row in rows:
        if row:
            t = {
                'id': row[0],
                'createUserId': row[1],
                'helpUserId':row[2],
                'isEnd':row[3],
                'createTime':row[4],
                'helpTime':row[5],
                'type':row[6],
                'receiveName':row[7],
                'receivePhone': row[8],
                'expressFirm':row[9],
                'getAddress':row[10],
                'getTime':row[11],
                'note':row[12],
                'tip':row[13],
                'sendAddress1':row[14],
                'sendAddress2':row[15]
            }
            res.append(t)
    return res


@trace
def get_event_by_user(params):
    conn = create_connection(DATABASE)
    user_id = params['user_id']
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM event WHERE createUserId=? ORDER BY createTime DESC", (user_id,))
        rows = cur.fetchall()
    res = []
    for row in rows:
        if row:
            t = {
                'id': row[0],
                'createUserId': row[1],
                'helpUserId':row[2],
                'isEnd':row[3],
                'createTime':row[4],
                'helpTime':row[5],
                'type':row[6],
                'receiveName':row[7],
                'receivePhone': row[8],
                'expressFirm':row[9],
                'getAddress':row[10],
                'getTime':row[11],
                'note':row[12],
                'tip':row[13],
                'sendAddress1':row[14],
                'sendAddress2':row[15]
            }
            res.append(t)
    return res


@trace
def get_event_by_receiver(params):
    conn = create_connection(DATABASE)
    user_id = params['user_id']
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM event WHERE helpUserId=? AND isEnd<>0 ORDER BY createTime DESC", (user_id,))
        rows = cur.fetchall()
    res = []
    for row in rows:
        if row:
            t = {
                'id': row[0],
                'createUserId': row[1],
                'helpUserId':row[2],
                'isEnd':row[3],
                'createTime':row[4],
                'helpTime':row[5],
                'type':row[6],
                'receiveName':row[7],
                'receivePhone': row[8],
                'expressFirm':row[9],
                'getAddress':row[10],
                'getTime':row[11],
                'note':row[12],
                'tip':row[13],
                'sendAddress1':row[14],
                'sendAddress2':row[15]
            }
            res.append(t)
    return res


if __name__ == '__main__':
    # params = {
    #     'createUserId': 123,
    #     'helpUserId':123,
    #     'isEnd':False,
    #     'createTime':'2019-4-10 19:20:23.223',
    #     'helpTime':'2019-4-10 20:20:23.223',
    #     'type':'快递',
    #     'receiveName':'李小雨',
    #     'receivePhone': '13804096493',
    #     'expressFirm':'中通',
    #     'getAddress':'学校篮球场',
    #     'getTime':'2019-4-11 12:00:00',
    #     'note':'取件号30',
    #     'tip':2,
    #     'sendAddress1':'1舍',
    #     'sendAddress2':'308号'
    # }
    # res = insert_event(params=params)
    # print(res)

    # events = get_event_list()
    # print(events)
#    res = insert_user('heihei', 'heiheiheihei')
#    print(res)
#    print(get_user_list())
#    print(get_cities_by_username('zhangshuyu'))
#    print(get_passwd_by_username('zhangshuyu'))
    params = {
        'user_id': '234'
    }
    res = get_event_by_user(params)
    print(res)
