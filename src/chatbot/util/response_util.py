from . import api_util as api
import json, os

location_map = {location["name"]: location["id"] for location in api.get_locations()["data"]}
course_map = {course["name"]: course["id"] for course in api.get_courses()["data"]}

locations_by_province = {
    "New Brunswick": ["LOAI FRANCHISE", "Life Start Saint John", "KHRYSPN FRANCHISE"],
    "Nova Scotia": ["Halifax", "Lisa Test", "testFranchise01", "testName001"]
}

def responses_factory(convo, response_key, user_params):

    if response_key == 'location':
        return handle_locations(convo, user_params)
    if response_key == 'course':
        return handle_courses(convo, user_params)
    if response_key == 'course_date':
        return handle_course_date(convo, user_params)
    else:
        return convo
    
def handle_locations(convo, user_params):
    locations = api.get_locations()
    location_names = locations_by_province[user_params['province']]
    
    # dynamically populate the reply array
    for location_name in location_names:
        convo["reply"].append({
            "question": location_name,
            
            "answer": convo["answer"]
        })
    
    del convo["answer"]
    
    return convo

def handle_course_date(convo, user_params):
    
    data = api.get_class_list(location_map[user_params['location']],
                                    course_map[user_params['course']])
    
    classes = data["data"][0]["courses"][0]["classes"]
    earliest_classes = classes[user_params['index']:user_params['index']+3]
    
    if not earliest_classes:
        path = os.path.join(os.path.dirname(__file__), "conversations", "find-course-dates/no_courses.json")
        user_params['index'] = 0
        with open(path, "r") as file:
            convo = json.loads(file.read())
        user_params['current_convo'] = convo
        user_params['answer'] = "no_courses.json"
        print(user_params)
        print('here')
        return convo["ice"]

    for class_info in earliest_classes:

        if class_info['vacancy'] > 0:
            msg = class_info["start_date"] if class_info["start_date"] == class_info["end_date"] else "{}-{}".format(class_info["start_date"], class_info["end_date"])

            convo["reply"].append({
                "question": msg,
                
                "answer": convo["answer"]
            })
        
    user_params['index'] = user_params['index'] + 3

    return convo

def handle_courses(convo, user_params):
    courses = api.get_courses()
    course_names = [course["name"] for course in courses["data"] if course["format"] == user_params['format']]
    
    # dynamically populate the reply array
    for course_name in course_names:
        convo["reply"].append({
            "question": course_name,
            
            "answer": convo["answer"]
        })
    
    del convo["answer"]
    return convo