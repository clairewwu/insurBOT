#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for insur_travel

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict

    Output:
        resultDICT    dict
"""
from ArticutAPI import Articut
from random import sample
import json
import os
import re

with open("account.info", encoding="utf-8") as f: #讀取account.info
    accountDICT = json.loads(f.read())


articut = Articut(accountDICT['username'], accountDICT['api_key'])



DEBUG_insur_travel = True
CHATBOT_MODE = False

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_insur_travel.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_insur_travel:
        print("[insur_travel] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR


def grab_info(inputSTR, pattern, resultDICT):
    userDefined = "intent/USER_DEFINED.json"
    posSTR = "".join([pos for pos in articut.parse(inputSTR, userDefinedDictFILE=userDefined)['result_pos'] if len(pos) > 1])
    # 取得比對之後的結果
    checkRes = ""
    for i in re.finditer(pattern, posSTR):
        checkRes = i.group()
        break

    # 取資訊加到resultDICT
    if checkRes:
        location = '<LOCATION>([^<]+)</LOCATION>' 
        for i in re.finditer(location, checkRes):
            resultDICT['location'] = i.group(1)
            break
        return resultDICT







def getResult(inputSTR, utterance, args, resultDICT, refDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "保旅平險":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "保旅遊相關的險":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "出去玩":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "到新竹參加活動":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            grab_info(inputSTR, args, resultDICT)
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "於國外旅行":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "於德國旅行":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            grab_info(inputSTR, args, resultDICT)
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    if utterance == "是一個海鷗族":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "travel" not in resultDICT['type']:
                resultDICT['type'].append("travel")
            

    return resultDICT