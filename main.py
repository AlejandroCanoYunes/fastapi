from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, Literal
from datetime import datetime
import requests

app = FastAPI()

origins = [
    "http://localhost:5173",
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

Duration = Literal['0 - 6 Months', '6 - 12 Months', '12+ Months']
PayFrequency = Literal['WEEKLY', 'BIWEEKLY', 'TWICEMONTHLY', 'MONTHLY']

class Summary(BaseModel):
    # info
    requested_amount: str
    product_purpose: Literal['Debt Consolidation', 'Credit Card Consolidation', 'Car Repair', 'Home Improvement', 'Utility Bill', 'School Expenses', 'Vacation', 'Emergency Expenses', 'Other']
    direct_deposit: Literal['yes', 'no']
    # contact-info
    dob: str
    canadian_status: Literal['pr', 'citizen', 'work_permit', 'student_visa', 'other']
    state: CanadianProvince
    city: str
    postal_code: str
    address: str
    monthly_income: int

    # living
    own_home: Literal['yes', 'no']
    rent_mortgage_payment: int
    property_value: Optional[int] = None
    property_mortgage: Optional[int] = None
    address_length_months: Literal[Duration]

    # financial
    credit_score: Literal['low', 'fair', 'good', 'unknown']
    in_bankruptcy:  Literal['yes', 'no']
    in_dmp:  Literal['yes', 'no']
    in_consumer_proposal:  Literal['yes', 'no']

    # income
    income_type: Literal['full_time', 'part_time', 'self_employed', 'retired', 'social_security', 'unemployed']
    job_title: str
    pay_date1: Optional[str] = None
    employer: Optional[str] = None
    time_at_job: Optional[Duration] = None
    work_phone: Optional[int] = None
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
    
    duration_mapping = {
        "0 - 6 Months" : 6,
        "6 - 12 Months": 12,
        "12+ Months": 24
    }
    
    data_dict['state'] = state_mapping[data_dict['state']]
    
    if data_dict["address_length_months"] is not None: 
        data_dict['address_length_months'] = duration_mapping[data_dict["address_length_months"]]
    
    if data_dict["time_at_job"] is not None:
        data_dict['time_at_job'] = duration_mapping[data_dict["time_at_job"]]
    
    if data_dict['work_phone'] is not None:
        data_dict['work_phone'] = str(data_dict['work_phone'])

    
    external_api_url = ""
    
    headers = {
            "authorizationToken": "",
            "Content-Type": "application/json"
        }

    response = requests.post(external_api_url, json=data_dict, headers=headers)
    
    print(data_dict)

    # Handle the response from the external API
    if response.status_code == 200:
        return {"message": "Application received and forwarded to external API", "data": data_dict}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    # return {"message": "Application received", "data": data_dict}