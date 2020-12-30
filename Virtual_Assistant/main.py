import speech_recognition # nhận lệnh từ speech sang text
# import pyttsx3 # chuyển text sang speech
from gtts import gTTS # chuyển text sang speech
import os
import playsound
import sys
import ctypes
import wikipedia
import datetime
import json
import webbrowser
import smtplib
import requests
import urllib
from googlesearch import search
import random
import re # tách domain để tìm kiếm web
import pyowm # weather
import time

class AI:
    dem=0
    #--------Nói--------------#
    def Speak(text):
        tts=gTTS(text,lang="vi")
        filename="voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    #--------Nghe-------------#
    def Ear():
        robot_ear = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as mic:
            robot_ear.adjust_for_ambient_noise(mic) # lọc tạp âm nhiễu môi trường
            print("Robot: Robot đang lắng nghe...")
            try:
                audio = robot_ear.listen(mic, timeout=5)  # lắng nghe, timeout
                you = robot_ear.recognize_google(audio, language="vi")
            except:
                you = ""
        return you
    #------------------Sleep------------------#
    def Sleep():
        AI.Speak("Bạn cần bao lâu")
        time.sleep(1)
        you = AI.Ear()
        if you:
            AI.Speak("OK mình đợi bạn")
            time.sleep(float(you))
        else:
            AI.Speak("Mình sẽ chờ cậu 5 giây")
            time.sleep(5)
    #----------Google_Search----------#
    def GGSearch(you):
        reg_ex = re.search('tìm kiếm (.+)',str(you).lower())
        if reg_ex:
            content = reg_ex.group(1)
            AI.Speak(content +" đang được tìm kiếm. Bạn vui lòng chờ một lát")
            url=[]
            for j in search(content, tld="co.in", num=10, stop=10, pause=2):
                url.append(j)
            webbrowser.open(str(url[random.randint(0,10)]))
        else:
            AI.Speak("Bạn muốn tìm kiếm gì")
        time.sleep(7)
    #-----------------Weather------------------------#
    def Weather():
        AI.Speak("Bạn muốn xem thời tiết ở đâu vậy")
        city=AI.Ear()
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        if city == "":
            city="Hà Nội"
        api_key = "78a4fd552139da5e53068e203eaa4a37"
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.datetime.now()
            content = """
                {city}
                Hôm nay là ngày {day} tháng {month} năm {year}
                Mặt trời mọc vào {hourrise} giờ {minrise} phút
                Mặt trời lặn vào {hourset} giờ {minset} phút
                Nhiệt độ trung bình là {temp} độ C
                Áp suất không khí là {pressure} héc tơ Pascal
                Độ ẩm là {humidity}%
                """.format(city=city,day=now.day, month=now.month,
                   year=now.year, hourrise=sunrise.hour,
                   minrise=sunrise.minute,
                   hourset=sunset.hour,
                   minset=sunset.minute,
                   temp=current_temperature,
                   pressure=current_pressure,
                   humidity=current_humidity)
            AI.Speak(content)
            time.sleep(3)
        else:
            AI.Speak("Không tìm thấy địa chỉ của bạn")
            AI.Weather()
    #-------------------------------Wikipedia---------------------------------------#
    def Wikipedia():

        time.sleep(3)
    #----------------------------main-----------------------------------------------------#
    def main():
        AI.Speak("Chào bạn tớ là Rybert. Tớ có thể giúp gì cho bạn")
        while True:
            you=AI.Ear()
            print(you)
            if you=="":
                AI.dem+=1
                if AI.dem==3:
                    AI.Speak("Nếu bạn không muốn nói gì thì thôi vậy, hẹn gặp lại.")
                    break
                AI.Speak("Tớ vẫn đang lắng nghe bạn đây. Bạn cần mình giúp gì không. Nếu không hãy nói tạm biệt.")
            elif "Xin chào" in you:
                AI.Speak("Chào bạn tớ là Rybert. Tớ có thể giúp gì cho bạn?")
            elif "tạm biệt" in you:
                AI.Speak("Tạm biệt bạn. Hẹn gặp lại.")
                break
            elif "Bạn tên" in you or "Tên bạn" in you or "Tên của bạn" in you:
                AI.Speak("Tên của tớ là Rybert. Tớ có thể giúp gì cho bạn.")
            elif "giờ" in you:
                AI.Speak("Bây giờ là " + datetime.datetime.now().strftime("%H:%M:%S")) # Time
                time.sleep(2)
            elif "ngày" in you:
                AI.Speak("Hôm nay là " + datetime.date.today().strftime("%d/%m/20%y"))   # Date
                time.sleep(2)
            elif "word" in you or "soạn thảo" in you:
                AI.Speak("Word đang được mở")
                os.startfile("C:\Program Files\Microsoft Office\Office16\WINWORD.EXE")  # Word
                time.sleep(7)
            elif "Excel" in you or "bảng tính" in you:
                AI.Speak("Excel đang được mở")
                os.startfile("C:\Program Files\Microsoft Office\Office16\EXCEL.EXE")   # Excel
                time.sleep(7)
            elif "PowerPoint" in you or "trình chiếu" in you:
                AI.Speak("PowerPoint đang được mở")
                time.sleep(7)
                os.startfile("C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE")  #PowerPoint
            elif "trình duyệt" in you:
                AI.Speak("Google Chrome đang được mở")
                os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")  # Open GG Chrome
                time.sleep(7)
            elif "YouTube" in you:
                AI.Speak("Youtube đang được mở")
                webbrowser.open("https://www.youtube.com")
                time.sleep(7)
            elif "Facebook" in you:
                AI.Speak("Facebook đang được mở")
                webbrowser.open("https://www.facebook.com")
                time.sleep(7)
            elif "Instagram" in you:
                AI.Speak("Instagram đang được mở")
                webbrowser.open("https://www.instagram.com")
                time.sleep(7)
            elif "email" in you:
                AI.Speak("Email đang được mở")
                webbrowser.open("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
                time.sleep(7)
            elif "Google Drive" in you:
                AI.Speak("Google drive đang được mở")
                webbrowser.open("https://www.google.com/intl/vi/drive")
                time.sleep(7)
            elif "Tìm kiếm" in you or "tìm kiếm" in you:
                AI.GGSearch(you)
            elif "thời tiết" in you or "Thời tiết" in you:
                AI.Weather()
            elif "là gì" in you:
                AI.Wikipedia()
            elif "chờ" in you:
                AI.Sleep()
            else:
                print("Tớ không hiểu cậu đang nói gì. Cậu muốn nói gì không?")
                AI.Speak("Tớ không hiểu cậu đang nói gì. Cậu muốn nói gì không?")
                time.sleep(1)

if __name__=="__main__":
    bot=AI
    bot.main()
























