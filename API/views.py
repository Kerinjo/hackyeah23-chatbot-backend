from django.http import JsonResponse
import json


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
