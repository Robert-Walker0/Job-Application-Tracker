from pydantic import BaseModel, ConfigDict
from utility_functions import to_camel_case

class JobApplication(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)
    company: str
    job_title: str
    date_applied: str
    platform: str = None
    link: str = None
    pay_type: str
    pay_amount: float = None
    notes: str = None
    status: str = "Applied"
    last_heard_from: str = None
