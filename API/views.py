from django.http import JsonResponse, HttpResponse
from .models import GeneratedUUID
from django.core.signals import request_finished
import json
import uuid
import pymongo
import datetime


client = pymongo.MongoClient("mongodb+srv://HOME:SAelfQuoQjxDmZc1@messagestorage.drak2ya.mongodb.net/?retryWrites=true&w=majority")

db = client['MessageStorage']
collection = db['Users']

# development only: uncomment to disable CSRF protection if needed
# from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def handle_message(request):
    mock_data = {
        "uuid": "encepence",
        "text": "terefere",
    }

    temp_message = {
        "isClient": True,
        "date": datetime.datetime.now(),
        "text": mock_data['text'],
    }

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message', '')

            temp_message = {
                "isClient": True,
                "date": datetime.datetime.now(),
                "text": message,
            }

            response_data = {'response': 'Response goes here'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)


def generate_uuid(request):
    try:
        # Generate new UUID
        new_uuid = uuid.uuid4()

        # Create document to insert into collection
        document = {
            'uuid': str(new_uuid),
            'history': {}
        }
        
        # Insert document into collection
        collection.insert_one(document)
        
        # Return the generated UUID as a response
        response_data = {'uuid': str(new_uuid)}
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def fetch_messages(request):
    uuid = request.GET.get('uuid')

    try:
        user = collection.find_one({'uuid': uuid})
        if user:
            return JsonResponse(user['history'], safe=False)
        else:
            return JsonResponse({'error': 'User UUID not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def purge(request):
    collection.remove()
    return HttpResponse('')


def add_body(request):
    user_uuid = "a75a392d-64f3-4c23-9db3-0c9682865ce3"

    mock_data = {
        "uuid": "encepence",
        "text": "terefere",
    }

    temp_message = {
        "isClient": True,
        "date": datetime.datetime.now(),
        "text": mock_data['text'],
    }

    new_history = [temp_message] * 5
    
    user = collection.find_one({'user_uuid': user_uuid})
    if user:
        try:
            collection.update_one(
                {'uuid': user_uuid},
                {'$set': {'history': new_history}}
            )
            print("History updated successfully.")
        except Exception as e:
            print("Error:", e)
    else:
        return JsonResponse({'error': 'User UUID not found'})

    return HttpResponse('')

def close_mongodb_client(sender, **kwargs):
    client.close()

request_finished.connect(close_mongodb_client)

