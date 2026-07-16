from utility_functions import to_camel_case, to_camel_case_dict


def test_to_camel_case():
    assert to_camel_case("is_true") == "isTrue"
    assert to_camel_case("job_title") == "jobTitle"
    assert to_camel_case("company") == "company"


def test_to_camel_case_dict():
    assert to_camel_case_dict(
        {"is_true": True, "job_title": "Cashier", "last_heard_from": "2026-07-06"}
    ) == {"isTrue": True, "jobTitle": "Cashier", "lastHeardFrom": "2026-07-06"}
    assert to_camel_case_dict(
        {"isAlreadyCamel": True, "isBrokenLaptop": False, "isPaintedAlready": False}
    ) == {"isAlreadyCamel": True, "isBrokenLaptop": False, "isPaintedAlready": False}


def test_to_camel_case_dict():
    assert to_camel_case_dict(
        {"is_true": True, "job_title": "Engineer", "last_heard_from": "2026-07-07"}
    ) == {"isTrue": True, "jobTitle": "Engineer", "lastHeardFrom": "2026-07-07"}
    assert to_camel_case_dict(
        {"is_popcorn_done": False, "current_time_in_microwave": 0, "number_of_pops": 0}
    ) == {"isPopcornDone": False, "currentTimeInMicrowave": 0, "numberOfPops": 0}


def test_to_camel_case_dict_already_camel():
    assert to_camel_case_dict({"company": "Google", "status": "Applied"}) == {
        "company": "Google",
        "status": "Applied",
    }
    assert to_camel_case_dict({"watermelon": True, "size": "huge", "cut": 3}) == {
        "watermelon": True,
        "size": "huge",
        "cut": 3,
    }
