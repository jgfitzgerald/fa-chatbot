from . import api_util as api

def responses_factory(convo, response_key):
    # dynamically populate location inputs
    if response_key == 'location':
        return handle_locations(convo)
    if response_key == 'course':
        return handle_courses(convo)
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
    courses = api.get_courses