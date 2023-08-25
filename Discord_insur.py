#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from insurance_bot import execLoki
from travel_reply import travel_reply, travel_reply_l2


logging.basicConfig(level=logging.DEBUG)


def getLokiResult(inputSTR): # 拿到的東西送去給Loki
    resultDICT = execLoki(inputSTR) # Loki結果的字典
    logging.debug("Loki Result => {}".format(resultDICT))
    return resultDICT

class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID): # MSC, multi session conversation 多輪對話
        '''
        清空與 messageAuthorID 之間的對話記錄
        '''
        templateDICT = self.templateDICT
        templateDICT["updatetime"] = datetime.now()
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.templateDICT = {"updatetime" : None,
                             "latestQuest": "",
                             "type":[]
        }
        self.mscDICT = { #userid:templateDICT
            
        }
        # ####################################################################################
        
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        logging.debug("收到來自 {} 的訊息".format(message.author))
        logging.debug("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
            logging.debug("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@{}> ".format(self.user.id), "").strip()
            logging.debug("人類說：{}".format(msgSTR))
            if msgSTR == "ping":
                replySTR = "pong"
            elif msgSTR == "ping ping":
                replySTR = "pong pong"

# ##########初次對話：這裡是 keyword trigger 的。
            elif msgSTR.lower() in ["哈囉","嗨","你好","您好","hi","hello"]: # 收斂（把變化量縮小）
                #有講過話(判斷對話時間差)
                if message.author.id in self.mscDICT.keys(): # 看這個人有沒有跟我們講過話
                    timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"]
                    #有講過話，但與上次差超過 5 分鐘(視為沒有講過話，刷新template)
                    if timeDIFF.total_seconds() >= 300:
                        self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                        replySTR = "嗨嗨，我們好像見過面，但卓騰的隱私政策不允許我記得你的資料，抱歉！"
                    #有講過話，而且還沒超過5分鐘就又跟我 hello (就繼續上次的對話)
                    else:
                        replySTR = self.mscDICT[message.author.id]["latestQuest"]
                #沒有講過話(給他一個新的template)
                else:
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                    replySTR = msgSTR.title() # 將第一個字大寫

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                resultDICT = getLokiResult(msgSTR)
                logging.debug("######\nLoki 處理結果如下：")
                logging.debug(resultDICT)

                if resultDICT:
                    # empty list in type
                    if not resultDICT['type']:
                        # type --> []
                        if len(resultDICT) == 1:
                            replySTR = "我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，您可描述您的需求(或自身狀況如年齡等等)，我們將為您提供諮詢，推薦您適合的保險~~"
                        
                        elif len(resultDICT) == 2 and "age" in resultDICT:
                           self.mscDICT[message.author.id]['age'] = True
                           replySTR = f"好的，您的年齡為{resultDICT['age'][0]}歲，為了幫助您: \n我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，或您可描述您的需求(或自身狀況等等)\n我們可以為您推薦適合您的保險以及方案！"
                        
                        
                        elif "unknown" in resultDICT:
                            # unknown + type
                            if len(resultDICT) == 2:
                                replySTR = "我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，您可描述您的需求(或自身狀況如年齡等等)，我們將為您提供諮詢，推薦您適合的保險~~" 
                            elif len(resultDICT) == 3 and ("low_budget" or "high_budget" or "age") in resultDICT:
                                if "low_budget" in resultDICT:
                                    self.mscDICT[message.author.id]['low_budget'] = True
                                    replySTR = "好的，已經幫您紀錄您想要比較經濟實惠一點的保險，\n我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，或您可描述您的需求(或自身狀況如年齡等等)\n我們可以為您推薦適合您的保險以及方案！"
                                elif "high_budget" in resultDICT:
                                    self.mscDICT[message.author.id]['high_budget'] = True
                                    replySTR = "好的，已經幫您紀錄您想要保障較多一點的保險，\n我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，或您可描述您的需求(或自身狀況如年齡等等)\n我們可以為您推薦適合您的保險以及方案！"
                                elif "age" in resultDICT:
                                    self.mscDICT[message.author.id]['age'] = True
                                    replySTR = f"好的，您的年齡為{resultDICT['age'][0]}歲，為了幫助您: \n我們提供三種網投保險諮詢服務:旅平險/意外傷害險/壽險，或您可描述您的需求(或自身狀況等等)\n我們可以為您推薦適合您的保險以及方案！"
                    else: 
                        # type has someting    
                        # first round
                        # only one type of insurance
                        if not self.mscDICT[message.author.id]['type']:
                            if len(resultDICT['type']) == 1:
                                if "travel" in resultDICT['type']:
                                    
                                    replySTR = travel_reply(resultDICT, message.author, self.mscDICT[message.author.id])
                                    print(self.mscDICT)
                                    pass
                                elif "life" in resultDICT['type']:
                                    pass
                                elif "accident" in resultDICT['type']:
                                    pass


                            # two or three insurances at the same time
                            elif len(resultDICT['type']) > 1:
                                for insur in resultDICT['type']:
                                    # check every condition one by one
                                    pass
                                            

                        else:# second round (to complete info)
                            # only one type of insurance
                            if "travel" in self.mscDICT[message.author.id]['type']:
                                replySTR = travel_reply_l2(resultDICT, self.mscDICT[message.author.id])
                                print(self.mscDICT)
                                pass
                            elif "life" in self.mscDICT[message.author.id]['type']:
                                pass
                            elif "accident" in self.mscDICT[message.author.id]['type']:
                                pass

                            # two or three insurances at the same time
                            elif len(self.mscDICT[message.author.id]['type']) > 1:
                                for insur in self.mscDICT[message.author.id]['type']:
                                    # check every condition one by one
                                    pass 

                else:
                    print("出了某些差錯")
            await message.reply(replySTR)
                         
            


if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
