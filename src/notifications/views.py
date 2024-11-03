# notifications/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import messaging
from .firebase_init import firebase_admin
import json

@csrf_exempt
def send_push_notification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get('title', 'New Notification')
        body = data.get('body', 'You have a new update!')

        # Generate or retrieve the FCM token
        fcm_token = generate_fcm_token()  # Implement as needed

        # Define the message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=fcm_token,
        )

        try:
            response = messaging.send(message)
            return JsonResponse({"success": True, "response": response}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
