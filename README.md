## qqpay-ptyhon-sdk

##  QQ钱包Python SDK
QQ钱包没有提供Python SDK。可能是因为用的太少，github上也没有完善的Python SDK。这里提供了一个简单的库，希望能够简化一些Python开发的流程。

QQ钱包服务端的接口签名方式暂时只支持MD5。目前实现了以下功能：
* 统一下单
* 通知验证
* 订单查询
* 申请退款
* 退款查询

## 使用教程
#### 安装

```
pip install dist/qqpay-ptyhon-sdk-0.0.1.tar.gz
```

#### 秘钥文件下载
```
```

#### 初始化
```python
    from qqpay import Qpay

    qpay = Qpay(
    appid="",
    mch_id="",
    api_key="",
    notify_url="",
    apiclient_cert_path="",
    apiclient_key_path=""
)
```

#### [统一下单](https://qpay.qq.com/qpaywiki/showdocument.php?pid=38&docid=58)
```python
result = qqpay.unified_order_apply(
    body=body,
    out_trade_no=out_trade_no,
    total_fee=total_fee,
    attach=attach,
    limit_pay="no_credit",
)
result = OrderedDict([('return_code', 'SUCCESS'),
             ('return_msg', 'SUCCESS'),
             ('retcode', '0'),
             ('retmsg', 'ok'),
             ('appid', '1231231231'),
             ('mch_id', '5678894'),
             ('nonce_str', 'xxxxxx'),
             ('prepay_id', 'xxxxxxxxxxx'),
             ('result_code', 'SUCCESS'),
             ('sign', 'qqwwxxxxxxx'),
             ('trade_type', 'APP')])
```
#### [通知验证](https://qpay.qq.com/qpaywiki/showdocument.php?pid=38&docid=59)
```python
result = qqpay.parse_payment_result(request.body.decode(encoding='UTF-8'))  # 签名验证
result = OrderedDict([('appid', '123xxxx'),
             ('attach', 'xxxx'),
             ('bank_type', 'BALANCE'),
             ('cash_fee', 1),
             ('fee_type', 'CNY'),
             ('mch_id', '456xxxx'),
             ('nonce_str', 'asdfqwexxxxxxx'),
             ('openid', 'wwwwxxxxxxxx'),
             ('out_trade_no', '345xxxxxx'),
             ('time_end', '20180308142331'),
             ('total_fee', 1),
             ('trade_state', 'SUCCESS'),
             ('trade_type', 'APP'),
             ('transaction_id', '14182151xxxxxxxxx'),
             ('sign', '05148606F187050Fxxxxxx')])
```
#### [订单查询](https://qpay.qq.com/qpaywiki/showdocument.php?pid=38&docid=60)
```python
# 接口请求
qqpay.query(transaction_id=transaction_id, out_trade_no=out_trade_no)
# 返回
OrderedDict([('return_code', 'SUCCESS'),
             ('return_msg', 'SUCCESS'),
             ('retcode', '0'),
             ('retmsg', 'ok'),
             ('appid', '110xxxxx'),
             ('attach', 'xxxx'),
             ('bank_type', 'BALANCE'),
             ('cash_fee', '1'),
             ('fee_type', 'CNY'),
             ('mch_id', '1418xxxx'),
             ('nonce_str', '370d3a34df30xxxxxx'),
             ('openid', '69E94503CAxxxxx'),
             ('out_trade_no', '18030814232xxxxx'),
             ('result_code', 'SUCCESS'),
             ('sign', '51FACF07F1D5BABC01xxxxx'),
             ('time_end', '20180308142331'),
             ('total_fee', '1'),
             ('trade_state', 'REFUND'),
             ('trade_state_desc', '已经产生退款'),
             ('trade_type', 'APP'),
             ('transaction_id', '14182151016011201xxxxx')])
```
#### [申请退款](https://qpay.qq.com/qpaywiki/showdocument.php?pid=38&docid=62)
```python
qqpay.refund(
        out_refund_no="",
        refund_fee="",
        op_user_id="",
        op_user_passwd="",
        transaction_id="",
        out_trade_no="")
 # 返回
OrderedDict([('return_code', 'SUCCESS'),
             ('return_msg', 'SUCCESS'),
             ('retcode', '0'),
             ('retmsg', 'ok'),
             ('appid', '110xxxx'),
             ('mch_id', '1418xxxx'),
             ('nonce_str', 'b47b30262xxxx'),
             ('openid', '69E94503CA8xxx'),
             ('out_refund_no', '1803081423xxxx'),
             ('out_trade_no', '1803xxxx'),
             ('refund_channel', 'ORIGINAL'),
             ('refund_fee', '1'),
             ('refund_id', '141821510170xxxx'),
             ('result_code', 'SUCCESS'),
             ('sign', '2C18F8E7EDExxxx'),
             ('total_fee', '1'),
             ('transaction_id', '1418215101601xxxx')])
```
#### [退款查询](https://qpay.qq.com/qpaywiki/showdocument.php?pid=38&docid=63)
```python
qqpay.query_refund(
            out_refund_no="",
            transaction_id="",
            out_trade_no="",
            refund_id="")
 # 返回
rderedDict([('return_code', 'SUCCESS'),
             ('return_msg', 'SUCCESS'),
             ('retcode', '0'),
             ('retmsg', 'ok'),
             ('appid', '1105884111'),
             ('cash_fee', '1'),
             ('cash_refund_fee_0', '1'),
             ('coupon_refund_fee_0', '0'),
             ('fee_type', 'CNY'),
             ('mch_id', '1418215101'),
             ('nonce_str', '5609d92e27f6cbd54758dfb5e4ea0283'),
             ('out_refund_no_0', '1803081423352vsIJze7nN3dxiYmDTOf'),
             ('out_trade_no', '18030814232109CWxudgPeX3io2Fz1Tl'),
             ('refund_channel_0', 'ORIGINAL'),
             ('refund_count', '1'),
             ('refund_fee_0', '1'),
             ('refund_id_0', '14182151017011201803081309325951'),
             ('refund_recv_accout_0', '用户余额'),
             ('refund_status_0', 'SUCCESS'),
             ('result_code', 'SUCCESS'),
             ('sign', '739557BD271D22C72F230BC47D9F7D43'),
             ('total_fee', '1'),
             ('transaction_id', '14182151016011201803081309325716')])
```


## Changelog
### 2018-03-08 (version 0.0.1)
