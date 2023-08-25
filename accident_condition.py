from insurance_bot import execLoki




def payContract(years):
    if years == 1:
        return ['心e路平安傷害保險', '刷平安一年定期意外身故傷害保險', '新iCarry傷害保險']
    else:
        return "不好意思，我們沒有提供超過1年意外險的服務喔！"



def age_filter_insur(age):
    age = int(age)
    possible_insur = []
    if 20 <= age <= 50:
        possible_insur.append("心e路平安傷害保險")
    if 18 <= age <=64:
        possible_insur.append("刷平安一年定期意外身故傷害保險")
    if 20 <= age <= 55:
        possible_insur.append("新iCarry傷害保險")
    else:
        possible_insur.append("no_insur")
    return possible_insur




def accident_insur(age, resultDICT):
    accident_feature = { 
                         "心e路平安傷害保險":['high_budget', 'job'],
                         "刷平安一年定期意外身故傷害保險":['low_budget', 'job'],
                         "新iCarry傷害保險": ['low_budget', 'traffic']

                        }

    possibleLIST = age_filter_insur(age)
    if len(possibleLIST) == 1:
        return possibleLIST
    else:
        final_prod = []
        productLIST = []
        match_ = [key for key in resultDICT if key in ['high_budget', 'job', 'low_budget', 'traffic']]
        for product, feature in accident_feature.items():
            # vague match
            if len(match_) == 1:
                if any(f in resultDICT for f in feature):
                    productLIST.append(product)

            # precise match
            elif len(match_) == 2:
                if all(f in resultDICT for f in feature):
                    productLIST.append(product)
                     
         
        # productLIST has two member need to compare (eg.['心e路平安傷害保險', '刷平安一年定期意外身故傷害保險'] )
        if len(productLIST) == 2:
            productLIST.extend(possibleLIST)
            # compare with age result, max insur 
            num = [productLIST.count(p) for p in productLIST]
            countDICT = dict(zip(productLIST, num))
            for p in countDICT:
                if countDICT[p] == max(list(countDICT.values())):
                    final_prod.append(p)
            return final_prod
        else:
            return productLIST


# 還有其他條件沒弄


if __name__ == "__main__":
    print(accident_insur(23, {"job":True, "age":['5'], "high_budget":True}))
                        







    # # three insur
    # if len(possibleLIST) == 3:
    #     if "job" in resultDICT:
    #         return "若是您是因為「職業」而想要有相關保障的話，傷害意外險的「心e路平安傷害保險」以及「刷平安一年定期意外身故傷害保險」方案很適合您！"
    #     else:
    #         if "high_budget" in resultDICT:
    #             return ["心e路平安傷害保險"]
    #         elif "low_budget" in resultDICT:
    #             return ["刷平安一年定期意外身故傷害保險"]
    #         else:
    #             if "traffic" in resultDICT:
    #                 return ["新iCarry傷害保險"]
    #             else:
    #                 return possibleLIST



    # # two insur
    # elif len(possibleLIST) == 2:
    #     if "心e路平安傷害保險" in possibleLIST and "刷平安一年定期意外身故傷害保險" in possibleLIST:
    #         if "job" in resultDICT:
    #             if "high_budget" in resultDICT:
    #                 return "心e路平安傷害保險"
    #             elif "low_budget" in resultDICT:
    #                 return "刷平安一年定期意外身故傷害保險"
    #         else:
    #             return 





    #     if possibleLIST == ['心e路平安傷害保險', '刷平安一年定期意外身故傷害保險']:
    #         if "high_budget" in resultDICT:
    #             return "心e路平安傷害保險"
    #         else:
    #             return
            
    #     elif possibleLIST == ['心e路平安傷害保險', '新iCarry傷害保險']:
    #         pass
    #     elif possibleLIST == ['刷平安一年定期意外身故傷害保險', "新iCarry傷害保險"]:
    #         pass


    # # one insur
    # elif len(possibleLIST) == 1:
    #     pass


# def acci_insurance(age, resultDICT):
    # age = int(age)

    # if 20 <= age <= 50:
    #     pass
    # elif 18 <= age <= 64:
    #     return "18足歲~64歲"
    # elif 20 <= age <= 55:
    #     return "20歲~55歲"
    # else:
    #     return "不在任何區間內"


