``` python
    import collpay
    
    collpay_obj = collpay.Collpay("0810545410c0dd7822cdd7c7caa336b2", collpay.ENV_SANDBOX, collpay.V1)
    
    response = collpay_obj.get_exchange_rate("USD", "BTC")
    print(response)
    
    response = collpay_obj.create_transaction({
        'type': 'collpay',
        'payment_currency': 'BTC',
        'order_currency': 'USD',
        'order_amount': '10',
        'payer_name': 'Xxx',
        'payer_email': 'xxx@gmail.com',
        'payer_phone': 'xxxxxxxx',
        'payer_address': 'Bangladesh 1216',
        'ipn_url': 'https://webhook.site/3b3ed4bf-8adb-4aec-b360-1d0c1c394766',
        'ipn_secret': 'Cf9mx4nAvRuy5vwBY2FCtaKr',   #Any random secret string of your's, It can be empty.
        'success_url': 'https://www.success.io/success.html',
        'cancel_url': 'https://www.failure.io/cancel.html',
        'cart': '{"item_name":"t-shirt","item_number":"23","invoice":"SDF-453672-PMT"}',   #Send any data format like json
        'webhook_data': '{"order_id":"ABC12345-12"}'    #Send any data format like json
    })
    print(response)
    
    response = collpay_obj.get_transaction("xxxxxxxxxxx")
    print(response)

```
