import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Product
import google.auth
from google.auth.transport.requests import Request

# Firebase settings
FCM_URL = 'https://fcm.googleapis.com/v1/projects/hrms-f4dab/messages:send'

from google.oauth2 import service_account
from google.auth.transport.requests import Request

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        "static/service_account.json",
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    credentials.refresh(Request())
    return credentials.token


@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')

        # Create the Product instance
        product = Product.objects.create(name=name, price=price)

        notification_data = {
            "message": {
                "topic": "all",
                "notification": {
                    "title": "Product Created Successfully",
                    "body": f"{product.name} has been added at price {product.price}!",
                }
            }
        }
        print("notification",notification_data)

        headers = {
            'Authorization': f'Bearer {get_access_token()}',
            'Content-Type': 'application/json; UTF-8'
        }

        response = requests.post(FCM_URL, headers=headers, data=json.dumps(notification_data))
        print("response",response)
        if response.status_code == 200:
            return JsonResponse({'message': 'Product created and notification sent successfully!'}, status=200)
        else:
            return JsonResponse({'message': 'Product created, but notification failed to send.'}, status=500)

    return render(request, 'create_product.html')
