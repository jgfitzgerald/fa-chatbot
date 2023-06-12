import yaml
import re

def substitute_variables(data, variables):
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

# def substitute_variables(data, variables):
#     pattern = r"\{\{([^}]+)\}\}"
#     substituted_data = re.sub(pattern, lambda match: get_substitution(match.group(1), variables), data)
#     return substituted_data


# def get_substitution(variable, variables):
#     value = variables.get(variable)
#     if isinstance(value, list):
#         return ", ".join(str(item) for item in value)
#     return str(value)


def process_yaml_file(file_path, data_map):
    with open(file_path) as file:
        yaml_content = file.read()

    substituted_content = substitute_variables(yaml_content, data_map)
    parsed_content = yaml.safe_load(substituted_content)

    return parsed_content