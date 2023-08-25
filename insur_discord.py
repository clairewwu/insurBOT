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
                             "latestQuest": ""
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
                    self.mscDICT[message.author.id]['type'] = []
                    replySTR = msgSTR.title() # 將第一個字大寫

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                resultDICT = getLokiResult(msgSTR)
                logging.debug("######\nLoki 處理結果如下：")
                logging.debug(resultDICT)
                
                if resultDICT:
                    # first round
                    if self.mscDICT[message.author.id]['type'] == []:
                        # when it cannot grab anything
                        if len(resultDICT) == 1 and resultDICT['type'] == []:
                            pass

                        # just ask the thing like 保保險
                        elif len(resultDICT) == 2 and 'unknown' in resultDICT:
                            pass

                        # only one type of insurance
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


                    
                    # second round (to complete info)
                    elif self.mscDICT[message.author.id]['type'] != []:
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
                    replySTR = "沒有"

            await message.reply(replySTR)
                         
            


if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
