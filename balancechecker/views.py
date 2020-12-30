from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Token
import urllib
import requests
from datetime import datetime, timedelta
from django.utils import timezone

AUTH_URL = 'https://auth.truelayer-sandbox.com/'
CLIENT_ID = 'sandbox-budgetingapp-a23a56'
CLIENT_SECRET = '9d170b4c-5e99-41a8-9996-3f6c2cf916e3'
REDIRECT_URI = 'https://localhost:8000/balance'

def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')

def get_token(request):
    CLIENT_DATA = {}
    data = request.GET
    code = data.get('code')

    body = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
    }

    res1 = requests.post('https://auth.truelayer-sandbox.com/connect/token', data=body)
    CLIENT_DATA['token'] = res1.json()
    # print(CLIENT_DATA['token'])

    access_token = CLIENT_DATA['token']['access_token']
    header = {'Authorization': f'Bearer {access_token}'}
    res2 = requests.get('https://api.truelayer-sandbox.com/data/v1/me', headers=header)
    CLIENT_DATA['credentials'] = res2.json()
    # print(CLIENT_DATA['credentials']['results'][0]['credentials_id'])

    token_data = Token(
        credentials_id = CLIENT_DATA['credentials']['results'][0]['credentials_id'],
        access_token=CLIENT_DATA['token']['access_token'],
        access_expires_in=timedelta(seconds = CLIENT_DATA['token']['expires_in']),
        refresh_token=CLIENT_DATA['token']['refresh_token']
        )
    token_data.user = request.user
    token_data.save()

    return access_token

def refresh_token(request):
    CLIENT_DATA = {}
    token_data = Token.objects.get(user=request.user)
    refresh_token = getattr(token_data, 'refresh_token')

    body = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
    }

    r = requests.post('https://auth.truelayer-sandbox.com/connect/token', data=body)

    CLIENT_DATA['token'] = r.json()
    access_token = CLIENT_DATA['token']['access_token']

    token_data.access_token = access_token
    token_data.access_expires_in = timedelta(seconds = CLIENT_DATA['token']['expires_in'])
    token_data.refresh_token = CLIENT_DATA['token']['refresh_token']
    token_data.save()

    return access_token

@login_required(login_url="/accounts/login/")
def balance(request):

    context = {}

    if 'code' in request.GET:

        access_token = get_token(request)

    else:
        token_data = Token.objects.get(user=request.user)

        if not token_data:
            query = urllib.parse.urlencode({
                'response_type': 'code',
                'client_id': CLIENT_ID,
                'scope': 'info accounts balance cards transactions direct_debits standing_orders offline_access',
                'redirect_uri': REDIRECT_URI,
                'providers': 'uk-ob-all uk-oauth-all uk-cs-mock',
            })

            context['auth_uri'] = f'https://auth.truelayer-sandbox.com/?{query}'
            return render(request, 'balance.html', context)
        else:
            access_token_expiry_date = getattr(token_data, 'access_updated_at') + getattr(token_data, 'access_expires_in')
            if access_token_expiry_date < timezone.now():
                access_token = refresh_token(request)
            else:
                access_token = getattr(token_data, 'access_token')

            auth_header = {'Authorization': f'Bearer {access_token}'}
            res = requests.get('https://api.truelayer-sandbox.com/data/v1/accounts', headers=auth_header)

            # blow up if cannot retrieve accounts
            res.raise_for_status()

            # process accounts
            accounts = {}
            for account in res.json()['results']:
                acc_id = account['account_id']
                acc_name = account['display_name']

                balance = retrieve_balance(acc_id, access_token)
                accounts[acc_id] = {
                    'balance': balance,
                    'name': acc_name,
                    }

            context['accounts'] = accounts.items()

    return render(request, 'balance.html', context)

def retrieve_balance(account_id, access_token) -> str:
    auth_header = {'Authorization': f'Bearer {access_token}'}
    res = requests.get(f'https://api.truelayer-sandbox.com/data/v1/accounts/{account_id}/balance', headers=auth_header)

    # blow up if cannot retrive balance for an account
    res.raise_for_status()

    balance = res.json()['results'][0]

    return {
        'currency': balance["currency"],
        'value': balance["available"],
    }
