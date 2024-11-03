# notifications/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import messaging
from .models import Product
from .firebase_init import firebase_admin  # Ensure firebase is initialized
import json

@csrf_exempt
def create_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        price = data.get("price")
        fcm_token = data.get("fcm_token")  # Optionally retrieve the FCM token

        # Create the Product object
        product = Product.objects.create(name=name, price=price, fcm_token=fcm_token)

        # Define notification message
        notification_title = "Product Created Successfully"
        notification_body = f"The product '{product.name}' has been added at ${product.price}!"

        # Send Firebase notification
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification_title,
                body=notification_body,
            ),
            token=fcm_token,  # Send to the provided token
        )

        try:
            response = messaging.send(message)
            return JsonResponse({"success": True, "response": response, "message": "Product created and notification sent"}, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
