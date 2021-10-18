import json

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


def clean_breakline(label,ignore_keys=[]):
    if type(label) is dict:
        for k,v in label.items():
            if k not in ignore_keys:
                label[k] = clean_breakline(v,ignore_keys)
    elif type(label) is list:
        for i in range(len(label)):
            label[i] = clean_breakline(label[i],ignore_keys)
    elif type(label) is str:
        return label.replace("\r\n","").replace("\n","")
    else:
        pass
    return label

def save(data,path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)