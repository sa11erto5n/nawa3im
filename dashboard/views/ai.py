from openai import OpenAI
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mistralai import Mistral

api_key = config('OPENROUTER_API_KEY')

import requests
import json
import base64
import logging

logger = logging.getLogger(__name__)

question = "How would you build the tallest building ever?"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
  "Authorization": f"Bearer {api_key}",
  "Content-Type": "application/json"
}

def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')
            
            if not question:
                return JsonResponse({'error': 'Question is required'}, status=400)
            
            payload = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": question}],
                "stream": True
            }

            response_content = ""
            with requests.post(url, headers=headers, json=payload, stream=True) as r:
                for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
                    buffer += chunk
                    while True:
                        try:
                            line_end = buffer.find('\n')
                            if line_end == -1:
                                break

                            line = buffer[:line_end].strip()
                            buffer = buffer[line_end + 1:]

                            if line.startswith('data: '):
                                data = line[6:]
                                if data == '[DONE]':
                                    break

                                try:
                                    data_obj = json.loads(data)
                                    content = data_obj["choices"][0]["delta"].get("content")
                                    if content:
                                        response_content += content
                                except json.JSONDecodeError:
                                    pass
                        except Exception:
                            break
            
            return JsonResponse({'response': response_content})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def analyze_image(request):
    if request.method == 'POST':
        try:
            logger.info("Received analyze_image request")
            
            try:
                data = json.loads(request.body)
                image_base64 = data.get('image_base64')
                image_type = data.get('image_type')
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            if not image_base64 or not image_type:
                logger.error("Missing required fields")
                return JsonResponse({'error': 'image_base64 and image_type are required'}, status=400)
            
            logger.info(f"Processing image of type: {image_type}, size: {len(image_base64)} bytes")
            
            # Initialize Mistral client
            api_key = config('MISTRAL_API_KEY')
            client = Mistral(api_key=api_key)
            model = "pixtral-12b-2409"
            
            messages = [
                {
                    "role":"system",
                    "content":"""you are a professional salesman.
                    you're goal is to write a custom products description using arabic language
                    you will provide the descrition only without any further explanation 
                    the description must follow the list style when mention the product features and must include emojies
                    the description text must be styled and include headlines and etc
                    """
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "descripe this image"
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:{image_type};base64,{image_base64}"
                        }
                    ]
                }
            ]
            
            # Get the chat response
            chat_response = client.chat.complete(
                model=model,
                messages=messages
            )
            
            response_content = chat_response.choices[0].message.content
            
            logger.info("Image analysis completed successfully")
            return JsonResponse({
                'status': 'success',
                'data': {
                    'description': response_content,
                    'language': 'ar'
                }
            })
            
        except Exception as e:
            logger.error(f'Error processing image: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

