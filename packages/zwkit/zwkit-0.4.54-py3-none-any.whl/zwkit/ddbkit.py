import dolphindb as ddb


def connect(self, userid='admin', passwd='123456'):
    s = ddb.session()
    s.connect(self.url, self.port, userid=userid, password=passwd)
    return s


def close_ddb(s):
    s.close()
