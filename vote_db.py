import sqlite3
import datetime

def init_db(db_name):
    conn = sqlite3.connect(db_name)
    print("opened database successfully")
    singlers=['吴宣仪', '孟美岐', 'Yamy', '周洁琼', '鞠婧祎', '李艺彤', '于文文', '陈意涵', '王菊', '苏诗丁']

    c = conn.cursor()
    for name in singlers:
        c.execute('''
            create table %s(
            vote_time datatime primary key,
             vote_num int
            );
        '''%name)

    print("create table successfully!")
    conn.commit()
    # conn.close()

class DB(object):
    def __init__(self, db_addr):
        self.addr = db_addr
        self.conn = sqlite3.connect(self.addr)
        self.c = self.conn.cursor()


    def close_db(self):
        self.conn.close()


    def reconnect_db(self):
        self.conn = sqlite3.connect(self.addr)
        self.c = self.conn.cursor()


    def insert(self, name, vote_num, data_time):
        self.exist_table(name)

        data_time = data_time.strftime("%Y-%m-%d %H:%M:%S") # yyyy-mm-dd hh:mm:ss
        data_time = str(data_time)

        sql_str = "insert into %s (vote_time, vote_num) values ('%s' , %d);" % (name, data_time, vote_num)
        self.c.execute(sql_str)
        self.conn.commit()


    def select_recent_record_by_name(self, name, rows=31):
        sql_str = '''
            select * from %s order by vote_time desc limit %d
        ''' % (name, rows)

        records = self.c.execute(sql_str)
        return records


    def exist_table(self, name):
        sql_str = '''
            create table if not exists %s(
            vote_time datatime primary key,
            vote_num int
            );
        ''' % name
        self.c.execute(sql_str)
        self.conn.commit()








def test():
    db = DB('test.db')
    db.insert('吴宣仪', 2000, datetime.datetime.now())

    db.select_recent_record_by_name("吴宣仪")
    db.exist_table('log')
    db.close_db()

if __name__ == "__main__":
    # test()
    init_db('asia_vote.db')