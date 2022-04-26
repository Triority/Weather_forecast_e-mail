import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
key='50ee3b0af9ea4375b2063e306dd4497b'

list = [["12345@qq.com",'100000','Triority']
]

def send(msg,rec_user):
    str1='successful.'
    str2='failure'
    mail_host="smtp.qq.com"
    send_user="12345@qq.com"
    send_pass="pass"
    message=MIMEText(msg,'plain','utf-8')
    message['from']=Header(send_user,'utf-8')
    message['to']=Header(rec_user,'utf-8')
    subject='今日份天气预报来咯'
    message['Subject']=Header(subject,'utf-8')
    try:
        smtpObj=smtplib.SMTP_SSL(mail_host,465)
        smtpObj.login(send_user,send_pass)
        smtpObj.sendmail(send_user,rec_user,message.as_string())
        print('succeed')
    except smtplib.SMTPException:
        print('error')


def get_time():
    tim=time.localtime(time.time())
    tm_year=tim[0]
    tm_mon=tim[1]
    tm_mday=tim[2]
    tm_hour=tim[3]
    tm_min=tim[4]
    tm_yday = tim[7]
    return tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday


def now_weather(key,location):
    url='https://devapi.qweather.com/v7/weather/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    now_temp = now_res_json['now']['temp']#温度
    now_feelsLike = now_res_json['now']['feelsLike']#体感温度
    now_windScale = now_res_json['now']['windScale']#风力等级
    now_windSpeed = now_res_json['now']['windSpeed']#风速
    now_windDir = now_res_json['now']['windDir']#风向
    now_text = now_res_json['now']['text']#描述
    now_obsTime = now_res_json['now']['obsTime']#观测时间
    return now_temp,now_feelsLike,now_windScale,now_windSpeed,now_windDir,now_text,now_obsTime


def today_weather(key,location):
    url='https://devapi.qweather.com/v7/weather/3d?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    sunrise = now_res_json['daily'][0]['sunrise']#日出时间
    sunset = now_res_json['daily'][0]['sunset']#日落时间
    moonrise = now_res_json['daily'][0]['moonrise']#月升时间
    moonset = now_res_json['daily'][0]['moonset']#月落时间
    tempMax = now_res_json['daily'][0]['tempMax']#当天最高温度
    tempMin = now_res_json['daily'][0]['tempMin']#当天最低温度
    textDay = now_res_json['daily'][0]['textDay']#白天天气状况
    textNight = now_res_json['daily'][0]['textNight']#晚间天气状况
    windDirDay = now_res_json['daily'][0]['windDirDay']#白天风向
    windScaleDay = now_res_json['daily'][0]['windScaleDay']#白天风力等级
    windSpeedDay = now_res_json['daily'][0]['windSpeedDay']#白天风速
    precip = now_res_json['daily'][0]['precip']#当天总降水量
    uvIndex = now_res_json['daily'][0]['uvIndex']#紫外线强度指数
    humidity = now_res_json['daily'][0]['humidity']#相对湿度
    return sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay, windScaleDay, windSpeedDay, precip, uvIndex, humidity


def now_air(key,location):
    url='https://devapi.qweather.com/v7/air/now?key='+key+'&location='+location
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    now_res=requests.get(url,headers=header)
    now_res_json=now_res.json()
    category = now_res_json['now']['category']#空气质量指数级别
    aqi = now_res_json['now']['aqi']#空气质量指数
    return category, aqi


def txt(key,location,name):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_yday = get_time()
    now_temp, now_feelsLike, now_windScale, now_windSpeed, now_windDir, now_text, now_obsTime = now_weather(key,location)
    sunrise, sunset, moonrise, moonset, tempMax, tempMin, textDay, textNight, windDirDay,  windScaleDay, windSpeedDay, precip, uvIndex, humidity = today_weather(key,location)
    category, aqi = now_air(key,location)
    msg = 'Dear '+name+':\n早安!\n'+\
          '今天是'+str(tm_year)+'年'+str(tm_mon)+'月'+str(tm_mday)+'日,是今年的第'+str(tm_yday)+'天了哦\n'+ \
          '\n下面是现在实时的天气状况:\n'+\
          '今天的空气状况为'+category+',质量指数为:'+aqi+'\n'+ \
          '当前室外天气是'+now_text+',气温'+now_temp+'度,体感温度'+now_feelsLike+'度,刮'+now_windDir+',风力'+now_windScale+'级,速度约'+now_windSpeed+'m/s\n'+\
          '以上信息的测量时间为'+now_obsTime+'\n'+\
          '\n下面是今天全天的天气情况:\n'+\
          '今天的最低气温是'+tempMin+'度,最高'+tempMax+'度,天气'+textDay+',刮'+windDirDay+',风力'+windScaleDay+'级,速度约'+windSpeedDay+'m/s\n'+\
          '预计今天总降水量为'+precip+'毫米,紫外线指数:'+uvIndex+',相对湿度为'+humidity+'%\n'+\
          '今天的日出时间是:'+sunrise+',日落时间:'+sunset+',月亮在'+moonrise+'升起,在'+moonset+'落下,今天夜晚天气'+textNight+'\n'+\
          '\nSincerely wish you all the best of luck today !!!\n                                                  Triority\n                                                  '+str(tm_year)+'.'+str(tm_mon)+'.'+str(tm_mday)
    return msg



for i in list:
    send(txt(key, i[1], i[2]), i[0])
