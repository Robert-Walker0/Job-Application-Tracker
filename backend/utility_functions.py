import json, io


def to_camel_case(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_camel_case_dict(application: dict) ->  dict:
    return {to_camel_case(key): value for key, value in application.items()}

def make_json_file(data, filename="applications.json"):
    """Helper that creates an in-memory JSON file for upload testing."""
    content = json.dumps(data).encode("utf-8")
    return {"file": (filename, io.BytesIO(content), "application/json")}

