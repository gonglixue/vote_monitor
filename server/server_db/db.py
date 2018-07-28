import sqlite3
import datetime

class ServerDB(object):
    def __init__(self, db_addr):
        self.addr = db_addr
        self.conn = sqlite3.connect(self.addr)
        self.c = self.conn.cursor()

        self._max_limit = 200


    # last 60 minutes vote_num
    def get_per_minute_vote(self, singer_name, minutes=60):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(minutes=minutes)
        query_from_time = current_time - delta_time # -3600s
        query_from_time = query_from_time.strftime("%Y-%m-%d %H:%M:%S")
        sql_str = "select * from %s where vote_time>='%s' order by vote_time limit %d" % (singer_name, query_from_time, self._max_limit)

        try:
            records = self.c.execute(sql_str) #[{"vote_time", "vote_num"}, {}, {}]
        except Exception as e:
            print(e)
            return []

        return self._calculate_increment_from_sequence(records.fetchall())

    def _calculate_increment_from_sequence(self, records_sequence):
        if len(records_sequence) <= 1:
            return []
        start_i = 0
        # for start_i in range(0, len(records_sequence)):
        #     if records_sequence[start_i]["vote_num"] >= 0:
        #         break

        for i in range(start_i+1, len(records_sequence)):
            cur_item = records_sequence[i]
            last_item = records_sequence[i-1]
            # next_item = records_sequence[i+1]
            increment = cur_item[1] - last_item[1]
            records_sequence[i] += (increment,)     # append an element to tuple

        records_sequence[start_i] += (-1, )
        return records_sequence[start_i+1:]

    def get_per_hour_vote(self, singer_name, hours=24):
        records = []
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(hours=hours)
        query_from_time = current_time - delta_time

        while True:
            query_time_str = query_from_time.strftime("%Y-%m-%d %H:%M:%S")
            sql_str = "select * from %s where vote_time>='%s' order by vote_time limit %d" \
            % (singer_name, query_time_str, self._max_limit)

            try:
                temp_records = self.c.execute(sql_str)
            except Exception as e:
                print(e)
                query_from_time = query_from_time + datetime.timedelta(hours=1)
                if query_from_time > current_time:
                    break
                continue

            temp_records = temp_records.fetchall()
            if len(temp_records) > 0:
                records.append(temp_records[0])
            else:
                fake_record = ('', -1)
                # records.append(fake_record)

            query_from_time = query_from_time + datetime.timedelta(hours=1)
            if query_from_time > current_time:
                break

        return self._calculate_increment_from_sequence(records)

    def get_latest_vote(self, name_list):
        '''
        return the nearest recorded vote_num
        :param name_list:
        :return: [(name, vote_num), ...], time_str
        '''
        records = []
        for name in name_list:
            sql_str = "select * from %s order by vote_time desc limit 1" % name
            try:
                record = self.c.execute(sql_str).fetchone() # tuple(vote_time, vote)
                nearest_record_time = record[0]
                record = (name, record[1])
            except Exception as e:
                print(e)
                record = (name, -1)

            records.append(record)

        return records, nearest_record_time

    def get_vote_given_gap(self, singer_name, gap_minutes=30, in_last_hours=12):
        records = []
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(hours=in_last_hours)
        query_from_time = current_time - delta_time

        while True:
            query_time_str = query_from_time.strftime("%Y-%m-%d %H:%M:%S")
            sql_str = "select * from %s where vote_time>='%s' order by vote_time limit 1" % (singer_name, query_time_str)

            try:
                temp_records = self.c.execute(sql_str)
            except Exception as e:
                print(e)
                query_from_time = query_from_time + datetime.timedelta(minutes=gap_minutes)
                if query_from_time > current_time:
                    break
                continue

            # query success
            temp_records = temp_records.fetchall()
            if len(temp_records) > 0:
                records.append(temp_records[0])
            else:
                fake_record = ('', -1)

            query_from_time = query_from_time + datetime.timedelta(minutes=gap_minutes)
            if query_from_time > current_time:
                break

        return self._calculate_increment_from_sequence(records)

    def test(self):
        sql_str = "select * from 吴宣仪 where vote_time>='2018-07-20 16:18:00' order by vote_time limit 100 "
        results = self.c.execute(sql_str)
        return results.fetchall()

def test():
    server_db = ServerDB("../../asia_vote.db")
    query_names = ['吴宣仪', '周洁琼', '孟美岐']
    real_time_votes, nearest_record_time = server_db.get_latest_vote(query_names)
    time_last = 60
    test_results = server_db.test()
    inc_results_1 = server_db.get_per_hour_vote('吴宣仪', hours=time_last)
    inc_results_2 = server_db.get_per_hour_vote('周洁琼', hours=time_last)
    inc_results_3 = server_db.get_per_hour_vote('孟美岐', hours=time_last)
    # inc_results = server_db.calculate_increment_from_sequence(results)

    counts = min(len(inc_results_1), len(inc_results_2))
    for ind in range(counts):
        item_1 = inc_results_1[ind]
        item_2 = inc_results_2[ind]
        item_3 = inc_results_3[ind]
        print('吴宣仪: %s %8d票（涨幅:%5d/hour）\t 周洁琼:%s %8d票（涨幅:%5d/hour）\t 孟美岐:%s %8d票（涨幅:%5d/hour）' %
              (item_1[0], item_1[1], item_1[2], item_2[0], item_2[1], item_2[2], item_3[0], item_3[1], item_3[2]))

    # for item in inc_results:
    #     print('%s \t 票数：%d \t %d涨幅:%d' % (item[0], item[1], 30, item[2]))

if __name__ == '__main__':
    test()