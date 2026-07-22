from pydantic import BaseModel, ConfigDict
from typing import Literal
from utility_functions import to_camel_case


class JobApplication(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)

    company: str
    job_title: str
    location: str
    priority: Literal["None", "Low", "Medium", "High"]
    work_type: Literal["On-Site", "Hybrid", "Remote"]
    date_applied: str
    platform: str = None
    link: str = None
    pay_type: Literal["Contract", "Hourly", "Salaried", "Internship"]
    pay_amount: float = None
    resume_name: str = None
    notes: str = None
    status: str = "Applied"
    last_heard_from: str = None


class JobApplicationUpdate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)

    company: str = None
    job_title: str = None
    location: str = None
    priority: str = None
    work_type: str = None
    date_applied: str = None
    platform: str = None
    link: str = None
    pay_type: str = None
    pay_amount: float = None
    resume_name: str = None
    notes: str = None
    status: str = None
    last_heard_from: str = None


class InterviewRound(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)

    round_label: str
    round_date: str
    notes: str = ""
