from typing import List
from pydantic import BaseModel
from .verdict import VerdictLabel

class TransferdocLabel(VerdictLabel):
    pass

class TransferdocInput(BaseModel):
    Type:str
    SFact:str
    Law:str
    Suspect:List[str]

class Transferdoc(BaseModel):
    input:TransferdocInput
    label:List[TransferdocLabel]