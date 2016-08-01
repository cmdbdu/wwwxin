# coding:utf8

from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
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

    message = wechat_instance.get_message()

    response = wechat_instance.response_text(
            content = (
                '感谢啊'
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
    return HttpResponse(response, content_type="application/xml")
