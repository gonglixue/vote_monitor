
import urllib.request
import urllib.parse
import re
import http.cookiejar
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
import time
from vote_db import DB


class FemaleList(object):
    def __init__(self, json_dict, current_time):
        self.femal_list = []
        self.current_time = current_time

        self._parse_json_dict(json_dict)

    def _parse_json_dict(self, json_dict):
        all_cards_list = json_dict["data"]["cards"]
        # print(self.current_time.strftime("%b-%d %H:%M:%S"), " 实时票数监控")
        # each 52-type card has 2 person
        female_card_list = all_cards_list[1]["card_group"]
        for card in female_card_list:
            if card["card_type"] != 52:
                continue
            card_items_list = card["items"] # with 2 person
            for person_item in card_items_list:
                print(person_item["title"], person_item["price2"])
                self.femal_list.append({"title": person_item["title"], "vote":person_item["price2"]})


def get_json_data_from_file(file_path):
    with open("response.json", "r") as f:
        json_txt = f.read()
        json_obj = json.loads(json_txt)
        print(json_obj["ok"])

        return json_obj

class App(object):
    def __init__(self, request_url, db_name):
        self.request_url = request_url
        self.db = DB(db_name)

    def _request(self):
        response = requests.get(self.request_url)
        json_dict = json.loads(response.text)
        female_list_obj = FemaleList(json_dict=json_dict, current_time=datetime.now())

        # print(female_list_obj.femal_list)
        return female_list_obj.femal_list, female_list_obj.current_time

    def _insert_list_to_db(self, female_list, date_time):
        for item in female_list:
            name = item['title']
            vote_num = item['vote'][0:-1]
            vote_num = int(vote_num.replace(',', ''))
            self.db.insert(name=name, vote_num=vote_num, data_time=date_time)


    def request_loop(self, delta_seconds=30):
        while True:
            female_list, date_time = self._request()
            self._insert_list_to_db(female_list, date_time)

            time.sleep(delta_seconds)

    def compare_2_request(self):
        print("\t实时票数监控")
        list_1, time_1 = self._request()
        time.sleep(30)
        list_2, time_2 = self._request()

        for i in range(len(list_1)):
            name = list_1[i]['title']
            vote_1 = list_1[i]['vote'][0:-1]
            vote_2 = list_2[i]['vote'][0:-1]
            vote_1 = int(vote_1.replace(',', ''))
            vote_2 = int(vote_2.replace(',', ''))

            print("%s\t%d票\t涨幅：%d/%ds" % (name, vote_2, (vote_2-vote_1), (time_2-time_1).seconds))


request_url = "https://m.weibo.cn/api/container/getIndex?uid=5650761945&wm=9006_2001&from=1087195010&sourcetype=qq&display=0&retcode=6102&containerid=1059030002_6800_42"


if __name__ == "__main__":
    vote_app = App(request_url, 'asia_vote.db')
    # vote_app.compare_2_request()
    vote_app.request_loop(60)