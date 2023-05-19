import yaml
import os
import logging as log
import uuid

# The Chatbot class takes in a file name and iterates through yaml files to dictate its conversational flow.
# Each yaml file contains one or 'more' tokens, which are essentially tasks.
# Each tasks typically displays a message, queries the user for input, processes the input in some way, and then proceeds to the next step in the sequence.
# The Chatbot will iterate through these yaml files until the next step is None, signifying the end of the conversation.
class Chatbot:
    def __init__(self):
        
        self.id = uuid.uuid4()
        self.scripts = []
        self.chat_history = []
        self.current_index = 0
        
        self.user_params = {}
        
        script_path = os.path.join(os.path.dirname(__file__), "scripts", 'intro_select_province.yaml') # TODO replace with const
        
        with open(script_path, "r") as file:
            self.current_script = yaml.safe_load(file)
            self.scripts.append(yaml.safe_load(file))

    # queue the next script
    def load_script(self, script_file):
        
        script_path = os.path.join(os.path.dirname(__file__), "scripts", script_file)
        with open(script_path, "r") as file:
            self.current_script = yaml.safe_load(file)
            self.current_index = 0
            self.scripts.append(yaml.safe_load(file))
            
    # process the first script
    def run(self):
        return { 'id': self.id, 'payload': self.process_token(self.current_script, 0) }
    
    # process an indivudal step in a script
    def process_token(self, script, index):
        current_token = script[index]
        messages = current_token['messages']
        
        response = []
        for msg in messages:
            
            response.append(msg)
            
            self.chat_history.append(('bot', msg))
            log.info('Bot: {}'.format(msg))

        payload = { 'response': response, 'input': script[index]['input'] }
        
        return payload
            
    # handles and stores user input
    def handle_input(self, input):
        
        outcomes = self.current_script[self.current_index]['outcome']  
        payload = []
        response = []
        
        matching_cases = [case for case in outcomes if input in case['cases']]
        case = matching_cases[0]
        payload = self.get_next(case['next'])
            
        if payload is not None:
            response = payload['response']
            if case['response'] is not None:
                response = case['response'].extend(response)  # Extend the list instead of appending
            
        print(case)
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
            
        # go to the next token in the same scripts
        elif isinstance(next_step_key, int):
            self.current_index = next_step_key
            return self.process_token(self.current_script, next_step_key)
        
        return None
                