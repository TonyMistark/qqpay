#!/usr/bin/env python
# coding: utf-8
import requests
import xmltodict
import logging
from xml.parsers.expat import ExpatError
from optionaldict import optionaldict

from .utils import random_string, dict_to_xml, calculate_signature, _check_signature
from .exceptions import InvalidSignatureException, QqPayException


logger = logging.getLogger(__name__)


class Base(object):

    def __init__(self, appid, mch_id, api_key, notify_url, apiclient_cert_path,
                 apiclient_key_path, api_base_url="https://qpay.qq.com/", nonce_str=None):
        self._appid = appid
        self._api_base_url = api_base_url
        self._mch_id = mch_id
        self._api_key = api_key
        self._apiclient_cert_path = apiclient_cert_path
        self._apiclient_key_path = apiclient_key_path
        self._notify_url = notify_url
        self._nonce_str = nonce_str

    @property
    def appid(self):
        return self._appid

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith('https://'):
            api_base_url = kwargs.pop('api_base_url', self._api_base_url)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint
        data = optionaldict(kwargs['data'])
        data.setdefault('mch_id', self._mch_id)
        data.setdefault('appid', self._appid)
        data.setdefault('nonce_str', self._nonce_str or random_string(32))
        data.setdefault("notify_url", self._notify_url)
        sign = calculate_signature(data, self._api_key)
        body = dict_to_xml(data, sign)
        body = body.encode('utf-8')
        kwargs['data'] = body

        # 商户证书
        kwargs['cert'] = (self._apiclient_cert_path, self._apiclient_key_path)

        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise reqe

        return self._handle_result(res)

    def _handle_result(self, res):
        res.encoding = 'utf-8'
        xml = res.text
        try:
            data = xmltodict.parse(xml)['xml']
        except (xmltodict.ParsingInterrupted, ExpatError):
            # 解析 XML 失败
            logger.debug('qq payment result xml parsing error', exc_info=True)
            return xml
        # return_code = data['return_code']
        # return_msg = data.get('return_msg')
        # result_code = data.get('result_code')
        # errcode = data.get('err_code')
        # errmsg = data.get('err_code_des')
        # if return_code != 'SUCCESS' or result_code != 'SUCCESS':
        #     # 返回状态码不为成功
        #     raise QqPayException(
        #         return_code=return_code,
        #         return_msg=return_msg,
        #         result_code=result_code,
        #         errcode=errcode,
        #         errmsg=errmsg
        #     )
        return data

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def check_signature(self, params):
        return _check_signature(params, self._api_key)

    def parse_payment_result(self, xml):
        """解析QQ支付结果通知"""
        try:
            data = xmltodict.parse(xml)
        except (xmltodict.ParsingInterrupted, ExpatError):
            raise InvalidSignatureException()

        if not data or 'xml' not in data:
            raise InvalidSignatureException()

        data = data['xml']
        sign = data.pop('sign', None)
        real_sign = calculate_signature(data, self._api_key)
        if sign != real_sign:
            raise InvalidSignatureException()

        for key in ('total_fee', 'settlement_total_fee', 'cash_fee', 'coupon_fee', 'coupon_count'):
            if key in data:
                data[key] = int(data[key])
        data['sign'] = sign
        return data
