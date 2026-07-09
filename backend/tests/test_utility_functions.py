from utility_functions import to_camel_case, convert_keys

def test_to_camel_case():
    assert to_camel_case("is_true") == "isTrue"
    assert to_camel_case("job_title") == "jobTitle"
    assert to_camel_case("company") == "company"

def test_convert_keys():
    assert convert_keys({"is_true", "job_title", "last_heard_from"} == {"isTrue", "jobTitle", "lastHeardFrom"})
    assert convert_keys({"isAlreadyCamel", "isBrokenLaptop", "isPaintedAlready"} == {"isAlreadyCamel", "isBrokenLaptop", "isPaintedAlready"}) 


def test_convert_keys():
    assert convert_keys({"is_true": True, "job_title": "Engineer", "last_heard_from": "2026-07-07"}) == {"isTrue": True, "jobTitle": "Engineer", "lastHeardFrom": "2026-07-07"}
    assert convert_keys({"is_popcorn_done": False, "current_time_in_microwave": 0, "number_of_pops": 0}) == {"isPopcornDone": False, "currentTimeInMicrowave": 0, "numberOfPops": 0}


def test_convert_keys_already_camel():
    assert convert_keys({"company": "Google", "status": "Applied"}) == {"company": "Google", "status": "Applied"}
    assert convert_keys({"watermelon": True, "size": "huge", "cut": 3}) == {"watermelon": True, "size": "huge", "cut": 3}