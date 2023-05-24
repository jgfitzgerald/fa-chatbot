import yaml
import re

def substitute_variables(data, variables):
    """
    The substitute_variables function takes a string and a dictionary of variables.
    It then replaces all occurrences of {{variable}} with the value in the dictionary.
    If the variable is not found, it will be replaced with an empty string.
    
    :param data: Pass in the data that needs to be substituted
    :param variables: Pass in the dictionary of variables that will be used to replace the variable placeholders
    :return: A string
    :doc-author: Trelent
    """
    pattern = r"\{\{(.*?)\}\}"
    
    def substitute(match):
        variable = match.group(1).strip()
        value = variables.get(variable)
        
        if isinstance(value, list):
            return "[" + ", ".join(f"'{item}'" for item in value) + "]"
        
        if isinstance(value, dict):
            return "{" + ", ".join(f"'{k}': '{v}'" for k, v in value.items()) + "}"
        
        return str(value)
    
    substituted_data = re.sub(pattern, substitute, data)
    return substituted_data

def process_yaml_file(file_path, data_map):
    with open(file_path) as file:
        yaml_content = file.read()

    substituted_content = substitute_variables(yaml_content, data_map)
    parsed_content = yaml.safe_load(substituted_content)

    return parsed_content