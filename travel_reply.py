from insurance_bot import execLoki
from ArticutAPI import Articut
import travel
import logging
import re



def travel_reply(resultDICT, person, recordDICT):
    recordDICT['type'].append("travel")
    print(resultDICT)
    if len(resultDICT['type']) == 1 and "travel" in resultDICT['type']:    
        # first time   # only one info
        if len(resultDICT) == 1:
            return f"好的！{person}您目前對旅平險有點興趣對嗎？那在麻煩您提供更多資訊(如：歲數、地點以及天數)，可以方便我們給您推薦更適合您的方案喔！"
        
        
        elif len(resultDICT) == 2:
            if "unknown" in resultDICT:
                return f"好的！{person}您目前對旅平險有點興趣對嗎？那在麻煩您提供更多資訊(如：歲數、地點以及天數)，可以方便我們給您推薦更適合您的方案喔！"
                

            elif "age" in resultDICT:
                recordDICT['age'] = resultDICT['age']
                return f"好的！{person}您目前想要保旅平險，且您的歲數為{resultDICT['age'][0]}歲，那想要問您其他資訊，如您期望的地點以及天數，以便我們幫您推薦喔～"
                
                
            elif "period" in resultDICT:
                recordDICT['period'] = resultDICT['period']
                pass
                
            elif "place" in resultDICT:
                recordDICT['place'] = resultDICT['place']
                place = travel.placeCheck(resultDICT['location'][0])
                return f"好的！{person}您目前想要保旅平險，您想要去的地點為{place}，那想要問您其他資訊，如您的歲數以及期望天數，以便我們幫您推薦喔～"
                
        elif len(resultDICT) == 3:
            # type + age + location
            if "age" in resultDICT and "location" in resultDICT:
                recordDICT['age'] = resultDICT['age']
                recordDICT['location'] = resultDICT['location']
                return f"謝謝您～再麻煩您提供「地點以及其天數」，以方便我們推薦更適合的方案給您喔～"
                
            # type + age + place
            elif "age" in resultDICT and "place" in resultDICT:
                recordDICT['age'] = resultDICT['age']
                recordDICT['place'] = resultDICT['place']
                return f"謝謝您～再麻煩您提供「地點以及其天數」，以方便我們推薦更適合的方案給您喔～"
                
            # type + place + period
            elif "place" in resultDICT and "period" in resultDICT:
                recordDICT['place'] = resultDICT['place']
                recordDICT['period'] = resultDICT['period']
                #place = travel.placeCheck(resultDICT['place'][0])
                #period = travel.periodCheck(resultDICT['period'][0])
                return f"謝謝您～目前您的訴求為去{resultDICT['place'][0]}{resultDICT['period'][0]}再麻煩您提供「歲數」，以方便我們推薦更適合的方案給您喔～"
                
                
        elif len(resultDICT) == 4:
            if "age" in resultDICT and "place" in resultDICT and "period" in resultDICT:
                recordDICT['age'] = resultDICT['age']
                recordDICT['place'] = resultDICT['place']
                recordDICT['period'] = resultDICT['period']
                # place = travel.placeCheck(resultDICT['place'][0])
                # period = travel.periodCheck(resultDICT['period'][0])
                # age = int(resultDICT['age'][0])
                precise_insur = travel.res_insurance(resultDICT['age'][0], resultDICT['period'][0], resultDICT['place'][0])
                del recordDICT['age'], recordDICT['place'], recordDICT['period']
                return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'
        return recordDICT
        



def travel_reply_l2(resultDICT, recordDICT):
        print("resultDICT", resultDICT)
        # second round (already have some record)
        # only one in recordDICT
        if "travel" in recordDICT['type']:
            if "age" in recordDICT:
                # take place & period
                if "place" in resultDICT and "period" in resultDICT:
                    #place = travel.placeCheck(resultDICT['place'][0])
                    # period = travel.periodCheck(resultDICT['period'][0])
                    # age = int(recordDICT['age'][0])
                    precise_insur = travel.res_insurance(recordDICT['age'][0], resultDICT['period'][0], resultDICT['place'][0])
                    del recordDICT['age']
                    return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'
                else:
                    return "您的資訊可能有缺漏喔！麻煩您提供完整的資訊，地點＋天數(例如：出國5天)"


                pass
                
            elif "location" in recordDICT:
                # take age & period
                if "age" in resultDICT and "period" in resultDICT:
                    place = travel.placeCheck(recordDICT['location'][0])
                    # period = travel.periodCheck(resultDICT['period'][0])
                    # age = int(resultDICT['age'][0])
                    precise_insur = travel.res_insurance(resultDICT['age'][0], resultDICT['period'][0], place)
                    del recordDICT['location']
                    return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'
                else:
                    return "您的資訊可能有缺漏喔！麻煩您提供完整的資訊，歲數+地點＋天數(例如：今年20歲，打算出國5天)"
                
            else:
                # no other thing in recordDICT
                if ("age" and "period" and "place") in resultDICT:
                    precise_insur = travel.res_insurance(resultDICT['age'][0], resultDICT['period'][0], resultDICT['place'][0])
                    return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'

                

        # two info in recordDICT
        elif len(recordDICT) == 2:
            if "age" in recordDICT and "place" in recordDICT:
                # take period
                # place = travel.placeCheck(recordDICT['place'][0])
                # period = travel.periodCheck(resultDICT['period'][0])
                precise_insur = travel.res_insurance(recordDICT['age'][0], resultDICT['period'][0], recordDICT['place'][0])
                del recordDICT['age'], recordDICT['place']
                return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'
                pass
                
            if "age" in recordDICT and "location" in recordDICT:
                place = travel.placeCheck(recordDICT['location'][0])
                # take period
                precise_insur = travel.res_insurance(recordDICT['age'][0], resultDICT['period'][0], place)
                del recordDICT['age'], recordDICT['location']
                return "根據您的需求幫您推薦 {} ，您可以參考官網的保費試算: {}".format(precise_insur, "http://") + '\n\n請問還有其他需求嗎？'
                pass







        # third round

if __name__ == "__main__":
             # output => {"key": ["今天天氣", "後天氣象"]}

    resultDICT = execLoki("我今年20歲，想要去韓國4天")
    recordDICT = {"type":['travel']}
    resultDICT = {"type":['travel']}
    print(resultDICT)
    res = travel_reply(resultDICT, "emily", recordDICT)
    print(res)
    #print(reply(resultDICT, "小明"))


    # recordDICT = {"type":['travel'], "age":["5"]}
    # resultDICT = {"place":['日本'], "period":["5天"]}
    # print(travel_reply_l2(resultDICT, recordDICT))