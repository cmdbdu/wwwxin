# coding:utf8

from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage,
                                ImageMessage,
                                VoiceMessage,
                                VideoMessage,
                                ShortVideoMessage,
                                LocationMessage,
                                LinkMessage,
                                EventMessage)
wechat_token = 'wwwxin'
wechat_appid = ''
wechat_appsecret = ''

wechat_instance = WechatBasic(
        token = wechat_token,
        appid= wechat_appid,
        appsecret = wechat_appsecret
        )
@csrf_exempt
def index(request):
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        if not wechat_instance.check_signature(
                signature=signature,
                timestamp=timestamp,
                nonce=nonce
                ):
            return HttpResponseBadRequest(' verift faild')
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError,e :
        return HttpResponseBadRequest('Invalid xml data')

    menu = ({
            'button':[
            {
                'type': 'click',
                'name': u'今日歌曲',
                'key': 'V1001_TODAY_MUSIC'
            },
            {
                'type': 'click',
                'name': u'歌手简介',
                'key': 'V1001_TODAY_SINGER'
            },
            {
                'name': u'菜单',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': u'搜索',
                        'url': 'http://www.soso.com/'
                    },
                    {
                        'type': 'view',
                        'name': u'视频',
                        'url': 'http://v.qq.com/'
                    },
                    {
                        'type': 'click',
                        'name': u'赞一下我们',
                        'key': 'V1001_GOOD'
                    }
                ]
            }
        ]})

    try:
        wechat_instance.create_menu(menu)
    except Exception,e:
        print e
    message = wechat_instance.get_message()

    response = wechat_instance.response_text(
            content = (
                u"""感谢您的关注。\n目前本订阅号功能单一，结构简单。\n请谅解!!"""
                )
            )
    if isinstance(message, TextMessage):
        content = message.content.strip()
        if content == "功能":
            replay_text = (
                    '功能可多了'
                    )
        elif content.endswith('a'):
            replay_text = (
                    'aa 毛线'
                    )
        else:
            replay_text = (
                    '不懂你在讲什么'
                    )
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, ImageMessage):
        replay_text = ('图片不能识别')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, VoiceMessage):
        replay_text = ('语言消息不能识别')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, ShortVideoMessage):
        replay_text = ('短视频消息不能识别')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, VideoMessage):
        replay_text = ('视频消息不能识别')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, LocationMessage):
        replay_text = ('位置消息不能识别')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, EventMessage):
        replay_text = ('这是什么事件')
        response = wechat_instance.response_text(content=replay_text)
    elif isinstance(message, LinkMessage):
        replay_text = ('连接么')
        response = wechat_instance.response_text(content=replay_text)
    return HttpResponse(response, content_type="application/xml")
