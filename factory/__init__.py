from data_model.verdict import Verdict, VerdictLabel, VerdictInput
from data_model.indictment   import Indictment, IndictmentLabel, IndictmentInput
from utils import get_license_plate_numbers, get_phone_numbers, get_accounts, clean_breakline, get_defendants

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
        verdictLabel = verdictLabel.dict()
        labels.append(clean_breakline(verdictLabel))

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

def createIndictment(data):
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
        label = IndictmentLabel(
            name = defendant,
            units = units,
            positions = positions,
            laws = laws,
            identities = identities,
            license_plate_number = license_plate_numbers,
            phone_number = phone_numbers,
            account = accounts
        )
        label = label.dict()
        labels.append(clean_breakline(label))

    #
    input_data = IndictmentInput(
        Type = 'TransferDoc2',
        SPSuspect = data['unlabelDoc'],
        SFact = '',
        Evidence = '',
        Law = '',
        FullText =  data['unlabelDoc']
    )

    verdict = Indictment(
        input = input_data,
        label = labels
    )

    return verdict