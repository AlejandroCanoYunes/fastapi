
const hello = {
  //loan info
  "requested_amount": 500,            // required (int), come from form : (string)
  "product_purpose": "Car Repair", 
  "direct_deposit": "yes",            // new (string)
  
  //contact info
  "dob": "yyyy-mm-dd",                // required (yyyy-mm-dd) (string 10) - display: DD-MM-YYYY - how it is: mm/dd/yyyy 
  "canadian_status": "citizen",
  "state": "BC",                      // new (string)
  "city": "Vancouver",                // new string(52)
  "postal_code": "323223",
  "address": "123 main st",           // new string(52)
  "monthly_income": 43333,
  
  //living situation
  "own_home": "yes",
  "rent_mortgage_payment": 43333,
  "property_value": 45555,
  "property_mortgage": 1000,
  "address_length_months": 6,           // new required int - comes in string (6+ months)
  
  //financial profile
  "credit_score": "good",
  "in_bankruptcy": "no",
  "in_dmp": "no",
  "in_consumer_proposal": "no",

  //income
  "income_type": "self employed",       // new (string)
  "job_title": "developer",
  "next_pay_date":  "2024-05-16",       // new date same as above
  "employer": "Pepe G",                 // new string(35)
  "time_at_job": 24,                    // new required int - comes in string (6+ months)
  "work_phone": "15304669559",
  "pay_frequency": "WEEKLY",            // new (string)

  //Debt
  "credit_card_debt_amount": 43333,
  "total_unsecured_debt": 43333,
  
  //privacy
  "consent_third_party_credit_authorization": "yes",
  
  //others
  "lang": "en",
  "email": "apphub@northstarbrokes.ca",
  "ip_address": "186.121.2.27",
  "first_name": "Ankush",
  "last_name": "Seth",
  "lead_id": "123456"
}

