import time
import datetime
from urllib import parse, request
import requests
import json

class WxReply(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextReply(WxReply):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """

        return XmlForm.format(**self.__dict)

class ImageReply(WxReply):
    def __init__(self, toUserName, fromUserName, mediaId=''):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
        <xml>
        <TuUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]</MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]</MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)

    def upload_image(self, local_path, access_token):
        upload_url = "https://api.weixin.qq.com/cgi-bin/media/upload"
        data = {'media': open(local_path, 'rb')}
        payload = {'access_token': access_token, 'type':'image'}
        
        res = requests.post(url=upload_url, params=payload, files=data)
        res = res.json()

        print("[{}] upload image response: {}".format(datetime.datetime.now(), json.dumps(res)))

        self.__dict['MediaId'] = res['media_id']
        return res['media_id']

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    appid = "wx70f90e8a09839906"
    secret = "8b452b3e83ce7b0e54c63beb39e03a49"
    query_str = "?grant_type=client_credential&appid={}&secret={}".format(appid, secret)

    req = request.Request(url=url+query_str)
    res = request.urlopen(req)
    res = res.read()
    res = json.loads(res.decode(encoding='utf-8'))
    print("[{}] get access token {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), res['access_token']))

    return res['access_token']


if __name__ == '__main__':
    access_token = get_access_token()
    replier = ImageReply('', '', '')
    media_id = replier.upload_image('/home/images/out.jpg', access_token)
    print("media_id: ", media_id)
