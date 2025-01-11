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
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("WORQHAT_API_KEY")}'
            }
            
            payload = {
                'question': prompt,
                'model': 'aicon-v4-nano-160824',
                'randomness': 0.5,
                'stream_data': True,
                'training_data': '',
                'response_type': 'text'
            }
            
            response = requests.post(
                'https://api.worqhat.com/api/ai/content/v4',
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return JsonResponse({
                    'content': response_data.get('content', ''),
                    'processingTime': response_data.get('processingTime', 0),
                    'processingId': response_data.get('processingId', ''),
                    'processingCount': response_data.get('processingCount', 0),
                    'conversation_id': response_data.get('conversation_id', ''),
                    'model': response_data.get('model', '')
                })
            else:
                return JsonResponse({
                    'error': f'API Error: {response.status_code}'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
