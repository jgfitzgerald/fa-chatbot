from . import api_util as api
import json, os

location_map = {location["name"]: location["id"] for location in api.get_locations()["data"]}
course_map = {course["name"]: course["id"] for course in api.get_courses()["data"]}
def responses_factory(convo, response_key, user_params):

    if response_key == 'location':
        return handle_locations(convo)
    if response_key == 'course':
        return handle_courses(convo)
    if response_key == 'course_date':
        return handle_course_date(convo, user_params)
    else:
        return convo
    
def handle_locations(convo):
    locations = api.get_locations()
    location_names = [location["name"] for location in locations["data"]]
    
    # dynamically populate the reply array
    for location_name in location_names:
        convo["reply"].append({
            "question": location_name,
            "answer": "handleInput",
            "next": convo["next"]
        })
    
    del convo["next"]
    
    return convo
    
def handle_courses(convo):
    courses = api.get_courses()
    course_names = [course["name"] for course in courses["data"]]
    
    # dynamically populate the reply array
    for course_name in course_names:
        convo["reply"].append({
            "question": course_name,
            "answer": "handleInput",
            "next": convo["next"]
        })
    
    del convo["next"]
    
    return convo

def handle_course_date(convo, user_params):
    
    data = api.get_class_list(location_map[user_params['location']],
                                    course_map[user_params['course']])
    
    classes = data["data"][0]["courses"][0]["classes"]
    earliest_classes = classes[user_params['index']:user_params['index']+3]
    
    if not earliest_classes:
        path = os.path.join(os.path.dirname(__file__), "conversations", "no_courses.json")
        with open(path, "r") as file:
            return json.load(file)["ice"]

    for class_info in earliest_classes:

        if class_info['vacancy'] > 0:
            msg = class_info["start_date"] if class_info["start_date"] == class_info["end_date"] else "{}-{}".format(class_info["start_date"], class_info["end_date"])

            convo["reply"].append({
                "question": msg,
                "answer": "handleInput",
                "next": convo["next"]
            })
        
    user_params['index'] = user_params['index'] + 3

    return convo


