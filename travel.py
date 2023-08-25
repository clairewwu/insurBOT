from insurance_bot import execLoki
from ArticutAPI import Articut
import cn2an
import json
import re


with open("account.info", encoding="utf-8") as f: #讀取account.info
    accountDICT = json.loads(f.read())
articut = Articut(accountDICT['username'], accountDICT['api_key'])


def placeCheck(place):
    counties = [
    "基隆",
    "台北",
    "新北",
    "桃園",
    "新竹",
    "苗栗",
    "台中",
    "彰化",
    "南投",
    "雲林",
    "嘉義",
    "台南",
    "高雄",
    "屏東",
    "宜蘭",
    "花蓮",
    "台東",
    "澎湖",
    "金門",
    "連江"
]
    if (place == "台灣" or place == "國內" or place in counties):
        return "國內"
    else:
        return "國外"


def periodCheck(period):
    if articut.parse(period)['result_obj'][0][0]['pos'] == "TIME_year":
        num = re.findall(r'(.)年', period)[0]
        if num.isalpha():
            return cn2an.cn2an(num) * 365
        else:
            return int(num) * 365
        
    elif articut.parse(period)['result_obj'][0][0]['pos'] == "TIME_month":
        num = re.findall(r'(.)個月', period)[0]
        if num.isalpha():
            return cn2an.cn2an(num) * 30
        else:
            return int(num) * 30
        
    elif articut.parse(period)['result_obj'][0][0]['pos'] == "TIME_day":
        num = re.findall(r'(.)天', period)[0]
        if num.isalpha():
            return cn2an.cn2an(num)
        else:
            return int(num)

        


def res_insurance(age, period, place):
    period = periodCheck(period)
    place = placeCheck(place)
    age = int(age)

    if age <= 7:
        if place == "國外":
            if period <= 180:
                return 'e悠遊旅行平安險'
            else:
                return "不好意思，我們國外旅平險沒有提供超過180天的保單服務喔！"
        elif place == "國內":
            if period <= 30:
                return 'e悠遊旅行平安險'
            else:
                return "不好意思，我們國內沒有提供這項保單服務喔！"
            

    elif age >= 20:
        if place == "國外":
            if period <= 180:
                return 'e悠遊旅行平安險'
            else:
                return "不好意思，我們國外旅平險沒有提供超過180天的保單服務喔！"
        elif place == "國內":
            if period <= 30:
                return 'e悠遊旅行平安險'
            elif period == 1:
                return '一日平安專案 & e悠遊旅行平安險'
            else:
                return "不好意思，我們國內沒有提供這項保單服務喔！"
        
        
    elif 20 < age < 70:
        if place == "國外":
            if period <= 180:
                return "不好意思，我們國外旅平險沒有提供超過180天的保單服務喔！"
            else:
                return None
        elif place == "國內":
            return "不好意思，我們國內沒有提供這項保單服務喔！"


def way_pay(inputSTR):
    if inputSTR:
        if inputSTR in ["信用卡", "活期帳戶", "街口電子支付"]:
            return '可以喔！我們有這種付費方式' 
        elif inputSTR == "電子支付":
            return "電子支付的話，我們只使用 街口電子支付"
        else:
            return "不好意思ㄟ～我們只有三種繳費方式: 信用卡 活期帳戶 街口電子支付"
    else:
        return ""
    

def ask_claim(inputSTR):
    if inputSTR:
        if inputSTR == True:
            return "關於保險賠償的部分\n海外的話有:\n\n身故/完全失能\n意外醫療\n海外突發疾病\n\n\n而國內有:身故/完全失能\n意外醫療"
    else:
        return ""








if __name__ == "__main__":

    resultDICT = execLoki("我需要去韓國一個月，請問我該保什麼保險")
    print(resultDICT['period'])
    print(periodCheck(resultDICT['period'][0]))

    