import os, uuid, json, re, copy
import logging as log
from util import api_util as api
from util import response_util as response_handler

class Chatbot:
    def __init__(self):
        
        self.id = uuid.uuid4()
        
        # empty map to hold user params
        self.user_params = {}
        self.user_params['index'] = 0
        
        self.current_convo = None
        self.current_token = None
        
    # initiates the first conversation, sends the first message
    def run(self):
        return self.load_convo('intro.json')
    
    # TODO
    def load_convo(self, convo):
        
        script_path = os.path.join(os.path.dirname(__file__), "util/conversations", convo)

        with open(script_path, "r") as file:
            convo = json.load(file)

        self.current_token = "ice" # ice is short for "ice breaker", the first convo token in a specific file
        
        substituted_content = self.sub_params(convo, self.current_token, self.user_params)

        self.current_convo = copy.deepcopy(substituted_content)

        # trucnate conversation to include only ui-required components
        temp = substituted_content[self.current_token].copy()

        if 'response_key' in temp:
            del temp['response_key']

        # delete each 'next' item as we don't need to return it
        for item in temp["reply"]:
            del item["next"]
            
        # return trucnated conversation
        return {"id": self.id, self.current_token: temp}
        
    # substitute placeholders in a conversation with user-inputted parameters
    def sub_params(self, convo, index, params):

        if 'course' in self.user_params:
            self.user_params['course_id'] = response_handler.course_map[self.user_params['course']] if self.user_params['course'] in response_handler.course_map else None

        def substitute(match):
            key = match.group(1)
            if key in params:
                return str(params[key])
            return match.group(0)

        pattern = r"\{\{([\w_]+)\}\}"
        data_str = json.dumps(convo)
        substituted_str = re.sub(pattern, substitute, data_str)

        substituted_data = json.loads(substituted_str)

        if 'response_key' in substituted_data[index]:
            substituted_data[index] = response_handler.responses_factory(substituted_data[index], substituted_data[index]['response_key'], self.user_params)

        return substituted_data
    
    # handles user input and returns the next conversation token
    def chat_input(self, input):

        # get the current conversation
        convo = self.current_convo[self.current_token]

        # Store the response if required
        if 'response_key' in convo:
            self.user_params[convo['response_key']] = input

        if any(input == reply["question"] for reply in convo["reply"]):
            answer = next((reply["next"] for reply in convo["reply"] if reply["question"].lower() == input.lower()), None)
        else:
            answer = convo['next']

        # load the next conversations
        if answer.endswith('.json'):
            self.load_convo(answer)
            return {"ice": self.current_convo[self.current_token]}
        else:
            self.current_token = answer
            # substitute params in the next conversation
            # make deep copy of convo, in case values get changed in future answers - want to keep the placeholders
            response = self.sub_params(copy.deepcopy(self.current_convo), self.current_token, self.user_params)

            return {"ice": response[self.current_token]}