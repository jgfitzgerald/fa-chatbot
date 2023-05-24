import requests
import os

API_URL = os.getenv('API_URL')
NUM_DISPLAY = 3

def handle_api_call(api_call):
    method = api_call['method']
    url = api_call['url']
    body = api_call.get('body')
    
    if method == 'GET':
        response = requests.get(url)
    elif method == 'POST':
        response = requests.post(url, json=body)
    # Add support for other HTTP methods if needed
    
    return response
        
def get_courses():
    response = requests.post(f'{API_URL}/api/courses/allcourses')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_locations():
    response = requests.post(f'{API_URL}/api/courses/locations')
    if response.status_code == 200:
        return response.json()
    else:
        return None