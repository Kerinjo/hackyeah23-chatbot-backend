from django.http import JsonResponse
from .models import GeneratedUUID
import json
import uuid
import pymongo
from django.core.signals import request_finished


client = pymongo.MongoClient("mongodb+srv://USER:eHrJbJtKHuEYZPh8@messagestorage.drak2ya.mongodb.net/?retryWrites=true&w=majority")

db = client['MessageStorage']
collection = db['Users']

# development only: uncomment to disable CSRF protection if needed
# from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def handle_message(request):
    if request.method == 'POST':
        try:
            # Assuming JSON
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message', '')

            # processing the message as needed goes here

            # Returning JSON response
            response_data = {'response': 'Response goes here'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)


def generate_uuid(request):
    try:
        # Generate new UUID
        new_uuid = uuid.uuid4()
        print(new_uuid)

        document = {
            'uuid': str(new_uuid),
            'history': {}
        }

        collection.insert_one(document)
        
        # Return the generated UUID as a response
        response_data = {'uuid': str(new_uuid)}
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def fetch_messages(request):
    user_uuid = request.GET.get('user_uuid')

    try:
        user = collection.find({'user_uuid': user_uuid})
        if user:
            return JsonResponse(user['history'])
        else:
            return JsonResponse({'error': 'User UUID not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def close_mongodb_client(sender, **kwargs):
    client.close()

request_finished.connect(close_mongodb_client)
