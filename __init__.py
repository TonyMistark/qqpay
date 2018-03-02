import time
from datetime import datetime, timedelta
from .base import Base
from .utils import timezone


class Qpay(Base):

    def unified_order_appy(self, out_trade_no, total_fee, trade_type="APP", limit_pay=None,
                           fee_type='CNY', time_start=None, time_expire=None, **kwargs):
        now = datetime.fromtimestamp(time.time(), tz=timezone('Asia/Shanghai'))
        hours_later = now + timedelta(hours=2)
        if time_start is None:
            time_start = now
        if time_expire is None:
            time_expire = hours_later
        data = {
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "trade_type": trade_type,
            "fee_type": fee_type,
            "time_start": time_start,
            "time_expire": time_expire
        }
        if limit_pay:
            data["limit_pay"] = limit_pay
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_unified_order.cgi", data=data)

    def query(self, **kwargs):
        data = {}
        data.update(kwargs)
        return self.post(url="cgi-bin/pay/qpay_order_query.cgi", data=data)
