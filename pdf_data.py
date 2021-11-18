from re import split
from pdfminer.high_level import extract_text
import re
import os
from decimal import Decimal

DIR = "/Users/saitouyuuki/Desktop/src/2021-exempt/"
exempt_d={}
exempts_l=[]

# Ticker Symb macher
ticker_r = re.compile(r"[0-9]{3}-[a-zA-Z]*")
# % macher for 「配当金等金額」「外国源泉徴収額」
delimiter_r = re.compile(r"%")
# date macher for 「配当金等金額(円)」「外国源泉徴収額(円)」
delimiter_r2 = re.compile(r"[0-9]{4}/[0-9]{2}/[0-9]{2}")

for filename in os.listdir(DIR):
    if filename.endswith(".pdf"): 
        dividend_b=False
        dividend_Yen_b=False
        gT_b=False
        counter=0
        #テキストの抽出
        text = extract_text(os.path.join(DIR, filename))
        lines=text.split('\n')
        #print(text)
        for line in lines:
            # ticker
            if re.match(ticker_r,line) != None:
                print("-----------------------")
                exempt_d['ティッカー']=re.match(ticker_r,line).group()
                counter=0
                dividend_b=True
                dividend_Yen_b=False
                gT_b=False
                print(re.match(ticker_r,line).group())

            # when gt shows up its time to get dividend and foriegn tax etc
            if re.match(delimiter_r,line) != None and dividend_b:
                #print(re.match(delimiter_r,line).group())
                counter=0
            if dividend_b:
                counter = counter + 1
            if line == 'gT' and dividend_b:
                gT_b = True
                counter = 0
            if not gT_b:
                if dividend_b and counter == 11 :
                    print(line)
                    exempt_d['配当金等金額']=line
                if dividend_b and counter == 13 :
                    print(line)
                    exempt_d['外国源泉徴収額']=line
            if gT_b:
                if dividend_b and counter == 4 :
                    print(line)
                    exempt_d['配当金等金額']=line
                if dividend_b and counter == 6 :
                    print(line)
                    exempt_d['外国源泉徴収額']=line

            # if date format shows up 
            if re.match(delimiter_r2,line) != None and dividend_b:
                #print(re.match(delimiter_r2,line).group())
                counter=0
                # 配当金等金額YENモードON
                dividend_Yen_b=True
                dividend_b=False
            if dividend_Yen_b:
                counter = counter + 1
            if dividend_Yen_b and counter == 7 :
                print(line)
                exempt_d['配当金等金額YEN']=line.replace(',','')
            if dividend_Yen_b and counter == 9 :
                print(line)
                exempt_d['外国源泉徴収額YEN']=line.replace(',','')
                #結果の保存
                exempts_l.append(exempt_d)
                exempt_d={}
print(exempts_l)

# 合計値の確認
配当金等金額_sum=Decimal(0.0)
外国源泉徴収額_sum=Decimal(0.0)
配当金等金額_yen_sum=Decimal(0.0)
外国源泉徴収額_yen_sum=Decimal(0.0)

for data in exempts_l:
    配当金等金額_sum=配当金等金額_sum + Decimal(data['配当金等金額'])
    外国源泉徴収額_sum=外国源泉徴収額_sum + Decimal(data['外国源泉徴収額'])
    配当金等金額_yen_sum=配当金等金額_yen_sum + Decimal(data['配当金等金額YEN'])
    外国源泉徴収額_yen_sum=外国源泉徴収額_yen_sum + Decimal(data['外国源泉徴収額YEN'])

print("---------確定申告に記載する値-------------")
print("配当金等金額->" + str(配当金等金額_sum) + "$")
print("外国源泉徴収額->" + str(外国源泉徴収額_sum) + "$")
print("配当金等金額YEN->" + str(配当金等金額_yen_sum) + "円")
print("外国源泉徴収額YEN->" + str(外国源泉徴収額_yen_sum) + "円")