from . import api_util as api
import json, os

location_map = {location["name"]: location["id"] for location in api.get_locations()["data"]}
course_map = {course["name"]: course["id"] for course in api.get_courses()["data"]}
course_formats = {course["name"]: course["format"] for course in api.get_courses()["data"]}

locations_by_province = {
    "New Brunswick": ["LOAI FRANCHISE", "Life Start Saint John", "KHRYSPN FRANCHISE"],
    "Nova Scotia": ["Halifax", "Lisa Test", "testFranchise01", "testName001"]
}

# replace this with an api endpoint in the future
class_id_link_map = {
    "701": "https://www.lifestarttraining.com/course/",
    "75": "https://www.lifestarttraining.com/course/",
    "73": "https://www.lifestarttraining.com/course/",
    "38": "https://www.lifestarttraining.com/course/hybrid-workplace-standard-first-aid-cpraed-level-c-2021-ktliaxno-6pgy3ukn",
    "21": "https://www.lifestarttraining.com/course/workplace-standard-first-aid-cpraed-level-c",
    "18": "https://www.lifestarttraining.com/course/hybrid-emergency-first-aid-cpraed-level-c-vruk9ox8-alcfk85d#schedules",
    "17": "https://www.lifestarttraining.com/course/emergency-first-aid-cpraed-level-c",
    "15": "https://www.lifestarttraining.com/course/hybrid-cpraed-level-c-vruk9ox8-n7odlqzx-a14zuyco",
    "16": "https://www.lifestarttraining.com/course/in-person-cpraed-level-c#schedules",
    "68": "https://www.lifestarttraining.com/course/virtual-new-brunswick-6-hour-skills-refresher?loc=moncton",
    "53": "https://www.lifestarttraining.com/course/new-brunswick-annual-skills-refresher-6pgy3ukn-ovb3chlx",
    "39": "https://www.lifestarttraining.com/course/hybrid-cpraed-level-hcp-vruk9ox8-n7odlqzx#schedules",
    "40": "lifestarttraining.com/course/marine-basic-first-aid#schedules",
    "36": "https://www.lifestarttraining.com/course/life-start-safe-tween-babysitting-program#schedules",
    "19": "https://www.lifestarttraining.com/course/virtual-recertification-emergency-first-aid-cpraed-level-c230110095340",
    "26": "https://www.lifestarttraining.com/course/virtual-infant-and-child-first-aid-awareness",
    "27": "https://www.lifestarttraining.com/course/virtual-heart-attack-awareness?loc=moncton",
    "43": "https://www.lifestarttraining.com/course/annual-skills-refresher#schedules",
    "72": "https://www.lifestarttraining.com/course/",
    "74": "https://www.lifestarttraining.com/course/advanced-level-medical-first-responder-2022-wkidiybc-pgrsfk0b#schedules"
}

def responses_factory(convo, response_key, user_params):

    if response_key == 'location':
        return handle_locations(convo, user_params)
    if response_key == 'course':
        return handle_courses(convo, user_params)
    if response_key == 'course_date':
        return handle_course_date(convo, user_params)
    if response_key == 'all_courses':
        return handle_all_courses(convo, user_params)
    else:
        return convo
    
def handle_locations(convo, user_params):
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
    
    classes = data["data"][0]["courses"][0]["classes"] if data.get("data") and data["data"][0].get("courses") and data["data"][0]["courses"] else None
    earliest_classes = classes[user_params['index']:user_params['index']+3] if classes is not None else None
    
    if not earliest_classes and (classes is None or user_params['input'] not in [class_info["start_date"] if class_info["start_date"] == class_info["end_date"] else "{}-{}".format(class_info["start_date"], class_info["end_date"]) for class_info in classes]):
        path = os.path.join(os.path.dirname(__file__), "conversations", "find-course-dates/no_courses.json")
        user_params['index'] = 0
        with open(path, "r") as file:
            convo = json.loads(file.read())
        user_params['current_convo'] = convo
        user_params['answer'] = "find-course-dates/no_courses.json"
        return convo["ice"]

    for class_info in earliest_classes:

        if class_info['vacancy'] > 0:
            msg = class_info["start_date"] if class_info["start_date"] == class_info["end_date"] else "{}-{}".format(class_info["start_date"], class_info["end_date"])

            convo["reply"].append({
                "question": msg,
                
                "answer": convo["answer"]
            })
        
    
    user_params['index'] = user_params['index'] + 3

    # reset the counter if the user selected a date
    if user_params['input'] in [class_info["start_date"] if class_info["start_date"] == class_info["end_date"] else "{}-{}".format(class_info["start_date"], class_info["end_date"]) for class_info in classes]:
        user_params['index'] = 0

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

def handle_all_courses(convo, user_params):
    courses = api.get_courses()
    course_names = [course["name"] for course in courses["data"]]
    
    # alter the response key name so the user input is stored under the 'course' key
    convo['response_key'] = 'course'

    # dynamically populate the reply array
    for course_name in course_names:
        convo["reply"].append({
            "question": course_name,
            
            "answer": convo["answer"]
        })
    
    del convo["answer"]
    return convo