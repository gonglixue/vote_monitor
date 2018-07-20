import sqlite3
import datetime

class ServerDB(object):
    def __init__(self, db_addr):
        self.addr = db_addr
        self.conn = sqlite3.connect(self.addr)
        self.c = self.conn.cursor()


    # last 60 minutes vote_num
    def get_per_minute_vote(self, singer_name, minutes=60):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(minutes=minutes)
        query_from_time = current_time - delta_time # -3600s
        query_from_time = query_from_time.strftime("%Y-%m-%d %H:%M:%S")
        sql_str = "select * from %s order by vote_time desc where vote_time > '%s'" % (singer_name, query_from_time)

        records = self.c.execute(sql_str) #[{"vote_time", "vote_num"}, {}, {}]
        return records

    def calculate_increment_from_sequence(self, records_sequence):
        for i in range(1, len(records_sequence)):
            cur_item = records_sequence[i]
            last_item = records_sequence[i-1]
            increment = cur_item["vote_num"] - last_item["vote_num"]
            records_sequence[i]["inc"] = increment

        return records_sequence


def test():
    current = datetime.datetime.now()
    delta_time = datetime.timedelta(minutes=30)
    last_time = current - delta_time
    print(last_time.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    test()