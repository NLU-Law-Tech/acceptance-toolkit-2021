from glob import glob
from loguru import logger
import argparse
import os
from typing import List
from pydantic import BaseModel
import json
# from VerdictCut import extract_fact

# args
parser = argparse.ArgumentParser()
parser.add_argument('to_format',choices=['verdict','indictment'])
parser.add_argument('-in_dir', default='./test_data')
parser.add_argument('-out_dir',default='./out_data')
args = parser.parse_args()
logger.debug(args)

assert os.path.isdir(args.in_dir)
os.makedirs(args.out_dir,exist_ok=True)

# utils
def get_defendants(data):
    """
    從標注資料中取出所有關係人
    """
    defendants = []
    for k,v in data.items():
        # logger.debug(k,v)
        if type(v) is dict:
            defendants += get_defendants(data[k])
        elif type(v) is list and k=='持有人':
            for defendant in v:
                defendant_name = defendant['val']
                # logger.debug(defendant_name)
                defendants.append(defendant_name)
        else:
            continue
    return list(set(defendants))


def _get_subjects(object,data,search_key):
    data = data[search_key] 
    all_license_plate_numbers = data.keys()
    outs = []
    for license_plate_number in all_license_plate_numbers:
        license_plate = data[license_plate_number]
        keepers = license_plate['持有人']
        for keeper in keepers:
            keeper_name = keeper['val']
            if keeper_name == object:
                outs.append(license_plate_number)
    return list(set(outs))

def get_license_plate_numbers(defendant,data):
    return _get_subjects(object=defendant,data=data,search_key='defendantsTagInfo')

def get_phone_numbers(defendant,data):
    return _get_subjects(object=defendant,data=data,search_key='phoneNumbersTagInfo')

def get_accounts(defendant,data):
    return _get_subjects(object=defendant,data=data,search_key='bankAccountsTagInfo')

def save(data,path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)

# data_model
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

def createVerdict(data):
    defendants = get_defendants(data)

    labels = []
    for defendant in defendants:
        # 單位, 職稱, 法條, 身份 並非這一次驗收目標**不進行轉換**
        units = []
        positions = []
        laws = []
        identities= []
        # 車牌 手機 銀行帳戶
        license_plate_numbers = get_license_plate_numbers(defendant,data)
        phone_numbers = get_phone_numbers(defendant,data)
        accounts = get_accounts(defendant,data)
        verdictLabel = VerdictLabel(
            name = defendant,
            units = units,
            positions = positions,
            laws = laws,
            identities = identities,
            license_plate_number = license_plate_numbers,
            phone_number = phone_numbers,
            account = accounts
        )
        labels.append(verdictLabel)

    #
    verdictInput = VerdictInput(
        Type = 'CourtVerdict',
        JAccused = ','.join(defendants),
        JMain = '' ,
        JFull = data['unlabelDoc'],
        JLaw = '',
        JRela = '',
        JRla = ''
    )

    verdict = Verdict(
        input = verdictInput,
        label = labels
    )

    # logger.debug(verdict)

    return verdict

if __name__ == '__main__':
    files = glob(os.path.join(args.in_dir,"*.json"))
    format_type = args.to_format
    for file in files:
        file_name = os.path.basename(file)
        logger.info(f"f_name: {file_name} f_path: {file}")
        data = open(file,'r',encoding='utf-8').read()
        data = json.loads(data)
        if format_type == 'verdict':
            processed_data = createVerdict(data)
            processed_data = processed_data.dict()
            # logger.debug(processed_data)
            save(processed_data,os.path.join(args.out_dir,file_name))
        else:
            raise Exception('`format_type` error')

