#!/usr/bin/env python
# coding: utf-8
import time
from datetime import datetime, timedelta
from .base import Base
from .utils import timezone, get_external_ip, get_md5

__version__ = "0.0.1"


class Qpay(Base):

    def unified_order_apply(self, out_trade_no, total_fee, body, client_ip=None, attach=None,
                            trade_type="APP", limit_pay=None, fee_type='CNY', time_start=None,
                            time_expire=None, **kwargs):
        """
        统一下单
        :param out_trade_no: 商户订单号
        :param total_fee: 订单金额
        :param body: 商品描述
        :param client_ip: 终端IP
        :param attach: 附加数据
        :param trade_type: 支付场景 APP、JSAPI、NATIVE
        :param limit_pay: 支付方式限制 可以针对当前的交易，限制用户的支付方式，如：仅允许使用余额，或者是禁止使用信用卡(no_balance)
        :param fee_type: 货币类型定义 默认为人民币：CNY
        :param time_start: 订单生成时间
        :param time_expire: 订单超时时间
        :param kwargs:
        :return:
        """
        now = datetime.fromtimestamp(time.time(), tz=timezone('Asia/Shanghai'))
        hours_later = now + timedelta(hours=2)
        if time_start is None:
            time_start = now
        if time_expire is None:
            time_expire = hours_later
        data = {
            "out_trade_no": out_trade_no,
            "body": body,
            "attach": attach,
            "total_fee": total_fee,
            "trade_type": trade_type,
            "fee_type": fee_type,
            "time_start": time_start.strftime('%Y%m%d%H%M%S'),
            "time_expire": time_expire.strftime('%Y%m%d%H%M%S'),
            "spbill_create_ip": client_ip or get_external_ip()
        }
        if limit_pay:
            data["limit_pay"] = limit_pay
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_unified_order.cgi", data=data)

    def query(self, transaction_id=None, out_trade_no=None, **kwargs):
        """
        订单查询
        :param transaction_id: QQ钱包订单号 QQ钱包订单号，优先使用。请求30天或更久之前支付的订单时 2选1
        :param out_trade_no: 商户订单号 商户系统内部的订单号,32个字符内、可包含字母，说明见商户订单号,当没传入transaction_id时必须传该参数
        :param kwargs:
        :return:
        """
        assert (transaction_id is not None) or (out_trade_no is not None), \
            "Both transaction_id and out_trade_no are None"
        data = {}
        if transaction_id:
            data["transaction_id"] = transaction_id
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_order_query.cgi", data=data)

    def close(self, out_trade_no, total_fee, **kwargs):
        """
        关闭订单
        :param out_trade_no: 商户订单号 商户系统内部的订单号,32个字符内、可包含字母。
        :param total_fee: 订单金额 订单总金额，单位为分，只能为整数
        :param kwargs:
        :return:
        """
        data = {"out_trade_no": out_trade_no, "total_fee": total_fee}
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_close_order.cgi", data=data)

    def refund(self, out_refund_no, refund_fee, op_user_id, op_user_passwd, transaction_id=None,
               out_trade_no=None,  refund_account=None, **kwargs):
        """
        申请退款
        :param out_refund_no: 商户退款单号 商户系统内部的退款单号，商户系统内部唯一，同一退款单号多次请求只退一笔
        :param refund_fee: 退款申请金额 本次退款申请的退回金额。单位：分。币种：人民币
        :param transaction_id: QQ钱包订单号 QQ钱包订单号，优先使用。请求30天或更久之前支付的订单时，此参数不能为空。
        :param out_trade_no: 商户订单号 商户系统内部的订单号,32个字符内、可包含字母
        :param op_user_id: 操作员ID 操作员帐号, 默认为商户号
        :param op_user_passwd: 操作员密码 只需传密码，底层已做MD5转换
        :param refund_account: 退款资金来源 EFUND_SOURCE_UNSETTLED_FUNDS---未结算资金退款（默认使用未结算资金退款
        :return:
        """
        assert (transaction_id is not None) or (out_trade_no is not None), \
            "Both transaction_id and out_trade_no are None"
        data = {
            "out_refund_no": out_refund_no,
            "refund_fee": refund_fee,
            "op_user_id": op_user_id,
            "op_user_passwd": get_md5(op_user_passwd),
        }
        if transaction_id:
            data["transaction_id"] = transaction_id
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        if refund_account:
            data["refund_account"] = refund_account
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_refund.cgi", data=data)

    def query_refund(self, refund_id=None, out_refund_no=None, transaction_id=None, out_trade_no=None):
        """
        退款查询
        :param refund_id: 4选1 QQ钱包退款单号 如果传入，则查询refund_id的退款详情，同时忽略out_refund_no参数
        :param out_refund_no: 4选1 在refund_id没有传入时，如果传入out_refund_no，则查询out_refund_no的退款详情
        :param transaction_id: 4选1 请求30天或更久之前支付的订单时，此参数不能为空。在refund_id，out_refund_no没有传入时，
                                如果传入transaction_id，则查询transaction_id相关的全部退款详情。transaction_id存在时，
                                则忽略out_trade_no
        :param out_trade_no: 4选1 商户订单号 在上面3项都没有传入时，则查询transaction_id相关的全部退款详情。以上4项必须传入一个。
        :return:
        """
        assert (refund_id is not None) or (out_refund_no is not None) or (transaction_id is not None) or (
                out_trade_no is not None),  "Both transaction_id and out_trade_no are None"
        data = {}
        if refund_id:
            data["refund_id"] = refund_id
        if out_refund_no:
            data["out_refund_no"] = out_refund_no
        if transaction_id:
            data["transaction_id"] = transaction_id
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        return self.post(url="cgi-bin/pay/qpay_refund_query.cgi", data=data)

