import xml.etree.ElementTree as ET

def parse_xml(wx_data):
    if len(wx_data) == 0:
        return None

    xmlData = ET.fromstring(wx_data)
    msg_type = xmlData.find('MsgType').text

    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)

class WxMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class TextMsg(WxMsg):
    def __init__(self, xmlData):
        super(TextMsg, self).__init__(xmlData)

        self.Content = xmlData.find('Content').text # string content

class ImageMsg(WxMsg):
    def __init__(self, xmlData):
        super(ImageMsg, self).__init__(xmlData)
        print(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
