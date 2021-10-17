from typing import List
from pydantic import BaseModel

class VerdictLabel(BaseModel):
    name:str
    units:List[str]
    positions:List[str]
    laws:List[str]
    identities:List[str]
    license_plate_number:List[str]
    phone_number:List[str]
    account:List[str]

class VerdictInput(BaseModel):
    Type:str
    JAccused:str
    JMain:str
    JFull:str
    JLaw:str
    JRela:str
    JRla:str

class Verdict(BaseModel):
    input:VerdictInput
    label:List[VerdictLabel]
