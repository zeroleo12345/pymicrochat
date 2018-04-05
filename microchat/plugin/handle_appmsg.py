import json
from .. import define
from .. import interface
from .. import mm_pb2
from .. import Util
from .  import plugin
from bs4 import BeautifulSoup
from .logger_wrapper import logger


# appmsg 消息处理
def appmsg_handler(msg):
    # 读取消息类型
    try:
        soup = BeautifulSoup(msg.raw.content,'html.parser')
        msg_type = soup.appmsg.type.contents[0]                     # 红包:<type><![CDATA[2001]]></type>
    except:
        pass

    if '2001' == msg_type:                                          # 红包消息
        if plugin.TEST_STATE[4]:                                    # 自动抢红包功能开关
            auto_recive_hb(msg)                                     # 自动抢红包
            qry_detail_wxhb(msg)                                    # 获取红包领取信息
    return


# 自动抢红包
def auto_recive_hb(msg):
    try:
        # 解析nativeUrl,获取msgType,channelId,sendId
        soup = BeautifulSoup(msg.raw.content,'html.parser')
        nativeUrl = soup.msg.appmsg.wcpayinfo.nativeurl.contents[0]
        msgType = Util.find_str(nativeUrl,'msgtype=','&')
        channelId = Util.find_str(nativeUrl,'&channelid=','&')
        sendId = Util.find_str(nativeUrl,'&sendid=','&')

        # 领红包
        (ret_code,info) = interface.receive_and_open_wxhb(channelId,msgType,nativeUrl,sendId)
        if not ret_code:
            logger.info('自动抢红包成功!', 11)
            logger.debug('红包详细信息:' + info)
        else:
            logger.info('红包详细信息:' + info, 13)
    except:
        logger.info('自动抢红包失败!')
    return

# 查看红包信息
def qry_detail_wxhb(msg):
    try:
        # 解析nativeUrl,获取sendId
        soup = BeautifulSoup(msg.raw.content,'html.parser')
        nativeUrl = soup.msg.appmsg.wcpayinfo.nativeurl.contents[0]
        sendId = Util.find_str(nativeUrl,'&sendid=','&')

        # 查看红包领取情况
        (ret_code,info) = interface.qry_detail_wxhb(nativeUrl, sendId)
        logger.info('查询红包详细信息:\n错误码:{}\n领取信息:{}'.format(ret_code, info), 13)
    except:
        logger.info('查看红包详细信息失败!', 13)
    return
