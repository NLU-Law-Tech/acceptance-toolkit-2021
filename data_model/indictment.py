from typing import List
from pydantic import BaseModel
from .verdict import VerdictLabel

class IndictmentLabel(VerdictLabel):
    pass

class IndictmentInput(BaseModel):
    Type:str
    SPSuspect:str
    SFact:str
    Evidence:str
    Law:str
    FullText:str

class Indictment(BaseModel):
    input:IndictmentInput
    label:List[IndictmentLabel]