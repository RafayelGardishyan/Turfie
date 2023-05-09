import json

config = json.loads(open('config.json', 'r').read())

def validate_string_length(string: str, min_length: int, max_length: int) -> bool:
    """
    Validates a string's length
    """
    return len(string) >= min_length and len(string) <= max_length

def check_contains(string: str, contains: str) -> bool:
    """
    Checks if a string contains any of the strings in the contains list
    """
    for contain in contains:
        if contain in string:
            return True
    return False

def validate_username(username: str) -> bool:
    """
    Validates a username
    """

    for element in config['username']['not_contains']:
        if check_contains(username, element):
            return False

    return validate_string_length(username, config['username']['min_length'], config['username']['max_length']) 


def validate_password(password: str) -> bool:
    """
    Validates a password
    """

    for element in config['password']['contains']:
        if not check_contains(password, element):
            return False
        
    return validate_string_length(password, config['password']['min_length'], config['password']['max_length'])

def validate_group_name(group_name: str) -> bool:
    """
    Validates a group name
    """

    for element in config['group_name']['not_contains']:
        if check_contains(group_name, element):
            return False

    return validate_string_length(group_name, config['group_name']['min_length'], config['group_name']['max_length'])