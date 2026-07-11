
def to_camel_case_dict(application: dict) ->  dict:
    return {to_camel_case(key): value for key, value in application.items()}

def to_camel_case(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])