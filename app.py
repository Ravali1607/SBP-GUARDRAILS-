from fastapi import FastAPI
from pydantic import BaseModel

from validator.HasValidURL_validator import URLValidator
from validator.secretspresent_validator import SecretValidator
from validator.Bias_validator import BiasValidator
from validator.cucumber_validator import CucumberValidator
from validator.profanity_validator import ProfanityValidator
from validator.pii_validator import PIIDetector
from validator.BannedWords_validator import BannedWordsValidator
from cucumber_expressions.parameter_type import ParameterType



app=FastAPI()

positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)
cucumber_validator = CucumberValidator(
    "I buy {positive_number} apple(s)/banana(s)/orange(s)",
    parameter_types=[positive_number]
)

validators={
    "url":URLValidator(),
    "secret":SecretValidator(),
    "bias":BiasValidator() ,
    "cucumberexp":cucumber_validator,
    "profanity":ProfanityValidator(),
    "detectpii":PIIDetector(),
    "bannedwords":BannedWordsValidator()
}

class RequestModel(BaseModel):
    text:str
    validator:str
    
@app.post("/validate")
def validate_text(request: RequestModel):

    validator = validators.get(request.validator)

    if not validator:
        return {
            "status": "error",
            "message": "Validator not supported"
        }

    return validator.validate(request.text)