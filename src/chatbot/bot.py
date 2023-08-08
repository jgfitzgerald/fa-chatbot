import os, uuid, json, re, copy
import logging as log
from util import api_util as api
from util import response_util as response_handler

class Chatbot:
    def __init__(self):
        
        self.id = uuid.uuid4()
        
        # empty map to hold user params
        self.chat_params = {}
        self.chat_params['index'] = 0
        
        self.chat_params['current_convo'] = None
        self.chat_params['current_token'] = None
        
    # initiates the first conversation, sends the first message
    def run(self):
        return self.load_convo('intro.json')
    
    # TODO
    def load_convo(self, convo):
        
        script_path = os.path.join(os.path.dirname(__file__), "util/conversations", convo)

        with open(script_path, "r") as file:
            convo = json.load(file)


        self.chat_params['current_token'] = "ice" # ice is short for "ice breaker", the first convo token in a specific file
        self.chat_params['current_convo'] = convo

        substituted_content = self.sub_params(convo, self.chat_params['current_token'], self.chat_params)

        # trucnate conversation to include only ui-required components
        temp = substituted_content[self.chat_params['current_token']].copy()

        if 'response_key' in temp:
            del temp['response_key']
            
        # return trucnated conversation
        return {"id": self.id, self.chat_params['current_token']: temp}
        
    # substitute placeholders in a conversation with user-inputted parameters
    def sub_params(self, convo, index, params):

        if 'course' in self.chat_params:
            self.chat_params['course_id'] = response_handler.course_map[self.chat_params['course']] if self.chat_params['course'] in response_handler.course_map else None
            self.chat_params['format'] = response_handler.course_formats[self.chat_params['course']] if self.chat_params['course'] in response_handler.course_map else None
            self.chat_params['reg_link'] = response_handler.class_id_link_map[self.chat_params['course_id']]
            
        def substitute(match):
            key = match.group(1)
            if key in params:
                return str(params[key])
            return match.group(0)

        pattern = r"\{\{([\w_]+)\}\}"
        data_str = json.dumps(convo)
        substituted_str = re.sub(pattern, substitute, data_str)
        index = re.sub(pattern, substitute, index)
        self.chat_params['current_token'] = index

        substituted_data = json.loads(substituted_str)

        if 'response_key' in substituted_data[index]:
            substituted_data[index] = response_handler.responses_factory(substituted_data[index], substituted_data[index]['response_key'], self.chat_params)
        
        return substituted_data
    
    # handles user input and returns the next conversation token
    def chat_input(self, input):
        
        # get the current conversation
        self.chat_params['input'] = input
        convo = self.sub_params(copy.deepcopy(self.chat_params['current_convo']), self.chat_params['current_token'], self.chat_params)
        convo = convo[self.chat_params['current_token']]
        
        # Store the response if required
        if 'response_key' in convo:
            self.chat_params[convo['response_key']] = input

        if 'course' in self.chat_params:
            self.chat_params['course_id'] = response_handler.course_map[self.chat_params['course']] if self.chat_params['course'] in response_handler.course_map else None
            self.chat_params['format'] = response_handler.course_formats[self.chat_params['course']] if self.chat_params['course'] in response_handler.course_map else None
            self.chat_params['reg_link'] = response_handler.class_id_link_map[self.chat_params['course_id']]
          
        if any(input == reply["question"] for reply in convo["reply"]):
            self.chat_params['answer'] = next((reply["answer"] for reply in convo["reply"] if reply["question"].lower() == input.lower()), None)
            self.chat_params['answer'] = re.sub(r"\{\{(\w+)\}\}", lambda match: self.chat_params.get(match.group(1), match.group(0)), self.chat_params['answer'])
        else:
            self.chat_params['answer'] = convo['answer'] if 'answer' in convo else self.chat_params['answer']
            self.chat_params['answer'] = re.sub(r"\{\{(\w+)\}\}", lambda match: self.chat_params.get(match.group(1), match.group(0)), self.chat_params['answer'])


        # load the next conversations
        if self.chat_params['answer'].endswith('.json'):
            new_convo = self.load_convo(self.chat_params['answer'])
            print(new_convo)
            print('here')
            return new_convo
        else:
            self.chat_params['current_token'] = self.chat_params['answer']
            # substitute params in the next conversation
            # make deep copy of convo, in case values get changed in future answers - want to keep the placeholders
            # self.chat_params['current_convo'] = self.sub_params(copy.deepcopy(self.chat_params['current_convo']), self.chat_params['current_token'], self.chat_params)

            subbed_convo = self.sub_params(copy.deepcopy(self.chat_params['current_convo']), self.chat_params['current_token'], self.chat_params)

            return {"ice": subbed_convo[self.chat_params['current_token']]}