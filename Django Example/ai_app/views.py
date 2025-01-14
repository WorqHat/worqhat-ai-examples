from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, 'ai_app/index.html')

@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        try:
            # Check if request body is empty
            if not request.body:
                return JsonResponse({'error': 'Request body is empty'}, status=400)
            
            # Log the raw request body for debugging
            print(f"Raw request body: {request.body}")
            
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as json_err:
                return JsonResponse({
                    'error': f'Invalid JSON format: {str(json_err)}',
                    'request_body': request.body.decode('utf-8')
                }, status=400)
            
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'}, status=400)
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("WORQHAT_API_KEY")}'
            }
            
            payload = {
                'question': prompt,
                'model': 'aicon-v4-nano-160824',
                'randomness': 0.5,
                'training_data': '',
                'response_type': 'text'
            }
            
            try:
                response = requests.post(
                    'https://api.worqhat.com/api/ai/content/v4',
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()  # Raise an exception for bad status codes
            except requests.RequestException as req_err:
                return JsonResponse({
                    'error': f'API Request Error: {str(req_err)}',
                    'status_code': getattr(response, 'status_code', None)
                }, status=500)
            
            try:
                response_data = response.json()
            except json.JSONDecodeError as json_err:
                return JsonResponse({
                    'error': f'Invalid API Response: {str(json_err)}',
                    'response_text': response.text
                }, status=500)
            
            return JsonResponse({
                'content': response_data.get('content', ''),
                'processingTime': response_data.get('processingTime', 0),
                'processingId': response_data.get('processingId', ''),
                'processingCount': response_data.get('processingCount', 0),
                'conversation_id': response_data.get('conversation_id', ''),
                'model': response_data.get('model', '')
            })
                
        except Exception as e:
            return JsonResponse({
                'error': f'Unexpected error: {str(e)}',
                'error_type': type(e).__name__
            }, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
