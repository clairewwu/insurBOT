from insurance_bot import execLoki
from travel_reply import travel_reply, travel_reply_l2





def getLokiResult(inputSTR): # 拿到的東西送去給Loki
    resultDICT = execLoki(inputSTR) # Loki結果的字典
    return resultDICT


