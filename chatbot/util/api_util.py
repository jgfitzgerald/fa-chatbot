import requests
import os

API_URL = os.getenv('API_URL')
NUM_DISPLAY = 3

def get_class_list(location_id, course_id):
    body = {"location":location_id, "course": course_id}
    print(body)
    response = requests.post(f'{API_URL}/api/courses/list', json = body)
    print(response.json)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
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