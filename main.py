from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import date

app = FastAPI()

origins = [
    "http://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

CanadianProvince = Literal[
    "BC - British Columbia",
    "ON - Ontario",
    "NL - Newfoundland and Labrador",
    "NS - Nova Scotia",
    "PE - Prince Edward Island",
    "NB - New Brunswick",
    "QC - Quebec",
    "MB - Manitoba",
    "SK - Saskatchewan",
    "AB - Alberta",
    "NT - Northwest Territories",
    "NU - Nunavut",
    "YT - Yukon",
    None
]

Duration = Literal['0 - 6 months', '6 - 12 months', '12+ months']
PayFrequency = Literal['WEEKLY', 'BIWEEKLY', 'TWICEMONTHLY', 'MONTHLY']

class Summary(BaseModel):
    # info
    requested_amount: str
    product_purpose: Literal['Debt Consolidation', 'Credit Card Consolidation', 'Car Repair', 'Home Improvement', 'Utility Bill', 'School Expenses', 'Vacation', 'Emergency Expenses', 'Other']
    direct_deposit: Literal['yes', 'no']
    # contact-info
    dob: str
    canadian_status: Literal['pr', 'citizen', 'work permit', 'student visa', 'other']
    state: CanadianProvince
    city: str
    postal_code: str
    address: str
    monthly_income: int

    # living
    own_home: Literal['yes', 'no']
    rent_mortgage_payment: int
    property_value: Optional[str] = None
    property_mortgage: Optional[str] = None
    address_length_months: Literal[Duration]

    # financial
    credit_score: Literal['low', 'fair', 'good', 'unknown']
    in_bankruptcy:  Literal['yes', 'no']
    in_dmp:  Literal['yes', 'no']
    in_consumer_proposal:  Literal['yes', 'no']

    # income
    income_type: Literal['full time', 'part time', 'self employed', 'retired', 'social security', 'unemployed']
    job_title: str
    pay_date1: Optional[str] = None
    employer: Optional[str] = None
    time_at_job: Optional[Duration] = None
    work_phone: Optional[str] = None
    pay_frequency: Optional[PayFrequency] = None
 
    # debt
    credit_card_debt_amount: int
    total_unsecured_debt: int

    # rest
    consent_third_party_credit_authorization: str
    email: EmailStr
    first_name: str
    last_name: str
    lead_id: str
    ip_address: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/submit-application/")
async def submit_application(data: Summary):
    data_dict = data.model_dump()
    data_dict['requested_amount'] = int(data_dict['requested_amount'])
    
    state_mapping = {
        "BC - British Columbia": "BC",
        "ON - Ontario": "ON",
        "NL - Newfoundland and Labrador": "NL",
        "NS - Nova Scotia": "NS",
        "PE - Prince Edward Island": "PE",
        "NB - New Brunswick": "NB",
        "QC - Quebec": "QC",
        "MB - Manitoba": "MB",
        "SK - Saskatchewan": "SK",
        "AB - Alberta": "AB",
        "NT - Northwest Territories": "NT",
        "NU - Nunavut": "NU",
        "YT - Yukon": "YT"
    }
    
    data_dict['state'] = state_mapping[data_dict['state']]
    
    return {"message": "Application received", "data": data_dict}