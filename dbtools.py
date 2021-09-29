import sqlite3
import os
from constants import db_file, data_folder
db_file = os.path.join(os.environ.get('ST_HOME'), db_file)


def connect():
    global conn

    timeout = 30

    # Note
    #  by default, sqlite is in autocommit mode,
    #  but the sqlite3 python module is *not* in autocommit mode by default
    #  we don't want autocommit mode, so we leave it at its default, which will result in a plain "BEGIN" statement
    #  (If you want autocommit mode, then set isolation_level to None)

    # open connection

    conn = sqlite3.connect(
        db_file,
        timeout,
    )
    return conn


def disconnect():
    global conn

    if is_connected():
        conn.close()

    conn = None


def is_connected():
    if not conn:
        return False
    else:
        return True


def resultset_to_dict(rs):
    kw = {}
    for column in list(rs.keys()):
        kw[column] = rs[column]
    return kw


def get_object_from_resultset(rs, class_):
    kw = resultset_to_dict(rs)
    return class_(**kw)


class BaseType:
    def get_full_local_path(self, prefix=data_folder):
        return os.path.join(self.local_path, prefix)


class File(BaseType):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        if self.status == 'error':
            buf = \
                "sdget_status={}," \
                "sdget_error_msg={}," \
                "error_msg='{}'," \
                "file_id={}," \
                "status={}," \
                "local_path={}," \
                "url={}".format(

                    self.sdget_status,
                    self.sdget_error_msg,
                    self.error_msg,
                    self.file_id,
                    self.status,
                    self.get_full_local_path(),
                    self.url,
                )

        else:
            buf = \
                "file_id={}," \
                "status={}," \
                "local_path={}," \
                "url={}".format(
                    self.file_id,
                    self.status,
                    self.get_full_local_path(),
                    self.url,
                )
        return buf