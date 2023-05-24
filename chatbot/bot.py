import yaml
import parser_util
import os
import logging as log
import uuid
import api_util
import task_handler

# The Chatbot class takes in a file name and iterates through yaml files to dictate its conversational flow.
# Each yaml file contains one or 'more' tokens, which are essentially tasks.
# Each tasks typically displays a message, queries the user for input, processes the input in some way, and then proceeds to the next step in the sequence.
# The Chatbot will iterate through these yaml files until the next step is None, signifying the end of the conversation.
class Chatbot:
    def __init__(self):

        course_ids = api_util.get_courses()
        location_ids = api_util.get_locations()

        self.id = uuid.uuid4()
        self.current_index = 0
        self.params = {}

        self.params['course_list'] = [item['name'] for item in course_ids['data']]
        self.params['location_list'] = [item['name'] for item in location_ids['data']]
        
        # script_path = os.path.join(os.path.dirname(__file__), "scripts", 'intro_select_province.yaml') # TODO replace with const
        
        # with open(script_path, "r") as file:
        #     self.current_script = yaml.safe_load(file)

    # queue the next script
    def load_script(self, script_file):
        
        script_path = os.path.join(os.path.dirname(__file__), "scripts", script_file)
        with open(script_path, "r") as file:
            yaml_content = file.read()
        
        substituted_content = parser_util.substitute_variables(yaml_content, self.params)
        self.current_script = yaml.safe_load(substituted_content)
        self.current_index = 0
            
    # process the first script
    def run(self):
        self.load_script('intro_select_province.yaml')
        return { 'id': self.id, 'payload': self.process_token(self.current_script, 0) }
    
    # process an indivudal step in a script
    def process_token(self, script, index):
        current_token = script[index]

        if isinstance(current_token['id'], str):
             return current_token
        else:
            messages = current_token['messages']
            
            response = []
            for msg in messages:
                
                response.append(msg)
                log.info('Bot: {}'.format(msg))

            payload = { 'response': response, 'input': script[index]['input'] }
            
            return payload
            
    # handles and stores user input
    def handle_input(self, input):

        outcomes = self.current_script[self.current_index]['outcome']
        input_data = self.current_script[self.current_index]['input']
        
        payload = []
        response = []
        
        matching_cases = [case for case in outcomes if input in case['cases']]
        case = matching_cases[0]
        payload = self.get_next(case['next'])
        
        # TODO this whole thing needs to be more understandable
        
        if 'id' in payload and isinstance(payload['id'], str):
            return task_handler.task_factory(self.id, payload)
        
        if 'store' in input_data and input_data['store'] is True:
            self.params[input_data['key']] = input
        if payload is not None:
            response = payload['response']
            if case['response'] is not None:
                response = case['response'].extend(response)  # Extend the list instead of appending
        return {
            "id": self.id,
            "payload": {
                "input": payload['input'] if payload is not None else None,
                "response": case['response']
            }
        }

    # loads the next script, or proceeds to the next token where applicable
    def get_next(self, next_step_key):
        if isinstance(next_step_key, str): 
                script_file = os.path.join(os.path.dirname(__file__), "scripts", next_step_key + ".yaml")
                if os.path.isfile(script_file):
                    self.load_script(next_step_key + ".yaml")
                    return self.process_token(self.current_script, self.current_index)
                else:
                    log.info("Script file '{}' not found.".format(next_step_key + ".yaml"))
                    return None
            
        # go to the next token in the same script   
        elif isinstance(next_step_key, int):
            self.current_index = next_step_key
            return self.process_token(self.current_script, next_step_key)
        
        return None


def task_factory(data):
    if data['id'] == 'find_courses':
        return execute_find_courses(data)
    else:
        raise ValueError("Unsupported 'id' type.")

def execute_find_courses(data):
    print("Executing number task...")
    # Implement the logic for the number task here

