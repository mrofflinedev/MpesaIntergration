from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html', {'navbar':'home'})


def token(request):
    access_token = MpesaAccessToken.get_access_token()
    return render(request, 'token.html', {'token': access_token})


def pay(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        amount = request.POST.get('amount', '').strip()

        if not phone or not amount:
            return HttpResponse('Missing phone number or amount', status=400)

        if not phone.startswith('254'):
            phone = '254' + phone.lstrip('+')

        access_token = MpesaAccessToken.get_access_token()
        timestamp, password = LipanaMpesaPpassword.generate_password()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': f'Bearer {access_token}'}

        payload = {
            'BusinessShortCode': LipanaMpesaPpassword.Business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone,
            'PartyB': LipanaMpesaPpassword.Business_short_code,
            'PhoneNumber': phone,
            'CallBackURL': 'https://example.com/callback',
            'AccountReference': 'Collins Wawire',
            'TransactionDesc': 'Web Development Charges',
        }

        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            return HttpResponse('success')
        return HttpResponse(response.text, status=response.status_code)

    return render(request, 'pay.html', {'navbar': 'stk'})


def stk(request):
    return render(request, 'pay.html', {'navbar':'stk'})