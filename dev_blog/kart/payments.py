from paytmpg import LibraryConstants,MerchantProperty,UserInfo,Money,EChannelId,EnumCurrency,PaymentDetailsBuilder,Payment
from random import random
from math import ceil
from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.utils import dateparse
from .models import PlacedOrder,PaymentDetail
from paytmchecksum import PaytmChecksum
import logging

def start() : 
    # For Staging 
    environment = LibraryConstants.STAGING_ENVIRONMENT

    # For Production 
    # environment = LibraryConstants.PRODUCTION_ENVIRONMENT

    # Find your mid, key, website in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    mid = "WorldP64425807474247" # "YOUR_MID_HERE"
    key = "kbzk1DSbJiV_O3p5" # "YOUR_KEY_HERE"
    website = "WEBSTAGING" # "YOUR_WEBSITE_NAME"
    client_id = "YOUR_CLIENT_ID_HERE" # 1

    callbackUrl = "http://127.0.0.1:8000/kart/payment/" # "MERCANT_CALLBACK_URL" 
    MerchantProperty.set_callback_url(callbackUrl)

    MerchantProperty.initialize(environment, mid, key, client_id, website)
    # If you want to add log file to your project, use below code
    file_path = './file.log'
    mode = "w"
    handler = logging.FileHandler(file_path, mode)
    formatter = logging.Formatter("%(name)s: %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    MerchantProperty.set_log_handler(handler)
    MerchantProperty.set_logging_disable(False)
    MerchantProperty.set_logging_level(logging.DEBUG)

start()

def startPayment(req) :
    if req.method == 'POST' : 
        name = req.POST.get('fName', '') +' '+ req.POST.get('lName')
        order = req.POST.get('itemsJson', '')
        email = req.POST.get('uEmail', '')
        phone = req.POST.get('uPhone','')
        price = req.POST.get('price', 0)
        address = req.POST.get('address1','') + ' ' + req.POST.get('address2')
        district = req.POST.get('district', '')
        state = req.POST.get('state', '')
        pin_code = req.POST.get('pin_code', '')
        if not price == 0 and not name == '' and not order == '{}' and not email == '' and not phone == '' and not pin_code == '':
            id = ceil(random()*1000000000000000 // 1)
            order = PlacedOrder(name=name,email=email, items_ordered=order, phone=phone, address=address,price=price,district=district,state=state,pin_code=pin_code,date=date.today(), order_id=id, order_status='u')
            order.save()
            print(name,order.id)
            channel_id = EChannelId.WEB
            order_id = str(id)
            txn_amount = Money(EnumCurrency.INR, str(price)+".00")
            user_info = UserInfo()
            user_info.set_cust_id(email)
            user_info.set_address(address)
            user_info.set_email(email)
            user_info.set_first_name(req.POST.get('fName', ''))
            user_info.set_last_name(req.POST.get('lName', ''))
            user_info.set_mobile(phone)
            user_info.set_pincode(pin_code)
            # initialize an Hash/Array
            paytmParams = {}

            paytmParams["MID"] = "WorldP64425807474247"
            paytmParams["ORDERID"] = str(id)

            # Generate checksum by parameters we have
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            paytmChecksum = PaytmChecksum.generateSignature(paytmParams, "kbzk1DSbJiV_O3p5")
            # print("generateSignature Returns:" + str(paytmChecksum))

            payment_details = PaymentDetailsBuilder(channel_id, order_id, txn_amount, user_info).build()
            response = Payment.createTxnToken(payment_details)
            return render(req, 'kart/payment.html', {'order_id': id, 'price': price, 'res': response }) # replace id by order.id
    return render(req, 'kart/checkout.html', {'success': False})
@csrf_exempt
def validate(req):
    # import checksum generation utility
    paytmChecksum = ""
    received_data = req.POST

    # Create a Dictionary from the parameters received in POST
    # received_data should contains all data received in POST
    paytmParams = {}
    for key, value in received_data.items(): 
        if key == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key] = value

    # Verify checksum
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    isValidChecksum = PaytmChecksum.verifySignature(paytmParams, "kbzk1DSbJiV_O3p5", paytmChecksum)
    if isValidChecksum:
        # Handle logic for successful or unsuccessful transactions later
        id = paytmParams["ORDERID"]
        code = paytmParams["RESPCODE"]
        order = PlacedOrder.objects.get(order_id=int(id))
        deatils = PaymentDetail(BANKNAME=paytmParams["BANKNAME"],BANKTXNID= paytmParams["BANKTXNID"],CURRENCY=paytmParams["CURRENCY"],GATEWAYNAME=paytmParams["GATEWAYNAME"],ORDERID=paytmParams["ORDERID"],PAYMENTMODE=paytmParams["PAYMENTMODE"],RESPCODE=paytmParams["RESPCODE"],RESPMSG=paytmParams["RESPMSG"],STATUS=paytmParams["STATUS"],TXNAMOUNT=paytmParams["TXNAMOUNT"],TXNID=paytmParams["TXNID"],TXNDATE=dateparse.parse_datetime(paytmParams["TXNDATE"])) 
        deatils.save()
        if code == "01":
            order.order_status="s"
            order.save(update_fields=['order_status'])
            return render(req, 'kart/checkout.html', {'success': True})
        else:
            order.order_status="f"
            order.save(update_fields=['order_status'])
            return render(req, 'kart/checkout.html', {'success': False})
    else:
        return render(req, 'kart/checkout.html', {'success': False})