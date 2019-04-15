# -*- coding: utf-8 -*-
import requests
import json
import datetime
import logging
import smtplib
import db

def main():
    email_list = db.get_all_email_city_list()
    key = '6c9855f23706490b98c5a7cfd41ed892'
#    email_list = [(u'yaoleiqi@qq.com', u'Yao Leiqi', u'CN101280601')]
    for email_info in email_list:
        try:
            email = email_info[0]
            username = email_info[1]
            city_id = email_info[2]
    
            url = 'https://free-api.heweather.com/s6/weather/now?location={0}&key={1}'.format(city_id, key)
    
            res = requests.get(url)
            data = json.loads(res.text)
            data = data['HeWeather6'][0]
    
            time = datetime.datetime.now()
            city = data['basic']['location']
            tmp = data['now']['tmp']
            cond = data['now']['cond_txt']
            wind_dir = data['now']['wind_dir']
            wind_sc = data['now']['wind_sc']
            msg = """
    亲爱的PiggyWeather用户{0}，您好，
    
    您当地的天气情况如下：
    {1}，当前时间是{2}，天气情况{3}
    当前温度{4}摄氏度，风向为{5}，风力大小{6}
    
    祝顺利
    PiggyWeather
            """.decode('utf-8').format(username, city, time, cond, tmp, wind_dir, wind_sc)
            logging.info(msg)
            SERVER = "smtp-mail.outlook.com"
            FROM = "Sar.Kerson@outlook.com"
            TO = [email] # must be a list
    
            SUBJECT = "PiggyWeather订阅邮箱提醒"
    
            # Send the mail
            server = smtplib.SMTP("smtp-mail.outlook.com", 587)
            server.ehlo()
            server.starttls()
            server.login(FROM, 'yao12345')
            server.sendmail(FROM, TO, msg.encode('utf-8'))
            server.close()
        except:
            continue

if __name__ == '__main__':
    main()

