from random import random
from paytmpg import LibraryConstants,MerchantProperty,UserInfo,Money,EChannelId,EnumCurrency,PaymentDetailsBuilder,Payment
from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging
from datetime import date
from .models import PlacedOrder
from kart.paytm import CheckSum
# import checksum generation utility
from paytmchecksum import PaytmChecksum

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

    callbackUrl = "http://127.0.0.1:8000/payment" # "MERCANT_CALLBACK_URL" 
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
            order = PlacedOrder(name=name,email=email, items_ordered=order, phone=phone, address=address,price=price,district=district,state=state,pin_code=pin_code,date=date.today())
            order.save()
            print(name,order.id)
            id = random()*1000000000000000 // 1
            channel_id = EChannelId.WEB
            order_id = str(id)
            txn_amount = Money(EnumCurrency.INR, "1.00")
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
            print("generateSignature Returns:" + str(paytmChecksum))

            payment_details = PaymentDetailsBuilder(channel_id, order_id, txn_amount, user_info).build()
            response = Payment.createTxnToken(payment_details)
            return render(req, 'kart/payment.html', {'order_id': id, 'price': price, 'res': response }) # replace id by order.id
    return render(req, 'kart/checkout.html', {'success': False})
@csrf_exempt
def validate(req):
    # import checksum generation utility
    print('hi')
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
    isValidChecksum = CheckSum.verify_checksum(paytmParams, "YOUR_KEY_HERE", paytmChecksum)
    if isValidChecksum:
        return render(req, 'kart/checkout.html', {'success': True})
    else:
        return render(req, 'kart/checkout.html', {'success': False})