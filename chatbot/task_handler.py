import api_util

course_ids = api_util.get_courses()
location_ids = api_util.get_locations()

courses = {item['name']: item['id'] for item in course_ids['data']}
locations = {item['name']: item['id'] for item in location_ids['data']}

def task_factory(id, data):
    if data['id'] == 'find_courses':
        return execute_find_courses(id, data)
    else:
        raise ValueError("Unsupported 'id' type.")

def execute_find_courses(id, data):
    location_name = data['params'][0]
    course_name = data['params'][1]

    location_id = locations[location_name]
    course_id = courses[course_name]

    course_response = api_util.get_class_list(location_id, course_id)
    return {
    "id": id,
    "payload": {
        "input": {
            "key": "date",
            "option_list": [
                course_response['data'][0]['courses'][0]['classes']
            ],
            "type": "buttons_single_select"
        },
        "response": [
            "Here are the next courses:"
        ]
    }
}