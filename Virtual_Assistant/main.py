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
from tkinter import *
from PIL import Image,ImageTk
from bs4 import BeautifulSoup
import imaplib
import threading


def Creat_widgets():
    t = Tk()
    t.title("Rybert")
    t.geometry("250x120+600+190")
    t.resizable(width=False, height=False)
    img = ImageTk.PhotoImage(Image.open("picAI.png"))
    panel = Label(t, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    t.mainloop()

class AI:
    dem = 0
    #--------Nói--------------#
    def Speak(text):
        tts=gTTS(text,lang="vi")
        #tts.speed(0.5)
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
        AI.Speak("Mình có thể chờ bạn tối đa là 30 giây. Bạn cần mình chờ bao lâu?")
        time.sleep(1)
        you = AI.Ear().replace(",",".")
        print(you)
        if you:
            tmp=you.split(" ")
            for i in tmp:
                if "giây" in you and i.isascii() and 0 < float(i) <= 30:
                    AI.Speak("OK mình sẽ chờ bạn "+i+" giây")
                    time.sleep(float(i))
                    break
        elif "tối đa" in you or "Tối đa" in you:
            AI.Speak("Ok mình sẽ chờ bạn 30 giây")
            time.sleep(30)
        else:
            AI.Speak("Mình sẽ chờ cậu 5 giây")
            time.sleep(5)
        AI.Speak("Bạn cần mình giúp gì không?")

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

    #-----------------Email--------------------------#
    def Email():
        user = "suppersiroo@gmail.com"
        pw = "lovestory99"
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(user, pw)
        status, messages = imap.select("INBOX")
        messages = int(messages[0])
        AI.Speak("Hộp thư đến hiện tại có %d thư chưa đọc, bạn có muốn xem hay không." %messages)
        you=AI.Ear()
        if "có" in you:
            AI.Speak("đang được mở")
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        else:
            AI.Speak("bạn không muốn xem thì thôi vậy. Bạn cần mình giúp gì nữa không?")

    #-----------------Weather------------------------#
    def Weather():
        AI.Speak("Bạn muốn xem thời tiết ở đâu vậy")
        city=AI.Ear()
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        if city == "": # link get location IP: https://dashboard.ipdata.co/
            r = requests.get('https://api.ipdata.co?api-key=f430d9660d9f5e8a11541a3ac01f09113dd8a0d2a910e4811301bd00').json()
            city=r['city']+','+r['country_name']
        api_key = "78a4fd552139da5e53068e203eaa4a37"
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            temperature = city_res["temp"]
            pressure = city_res["pressure"]
            humidity = city_res["humidity"]
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
                   temp=temperature,
                   pressure=pressure,
                   humidity=humidity)
            AI.Speak(content)
            time.sleep(2)
        else:
            AI.Speak("Không tìm thấy địa chỉ của bạn")
            AI.Weather()

    #-------------------------------Wikipedia---------------------------------------#
    def Wikipedia():
        AI.Speak("Bạn vui lòng nói từ khóa muốn tìm hiểu")
        you = AI.Ear()
        contents = wikipedia.summary(you).split(".")
        AI.Speak("Theo như mình tìm hiểu được thì")
        AI.Speak(contents[:2])
        AI.Speak("Vẫn còn đấy, bạn muốn nghe tiếp chứ")
        you = AI.Ear()
        if "có" in you or "" in you:
            AI.Speak(contents[2:])
        else:
            AI.Speak("Nếu cậu không muốn nghe tiếp thì thôi vậy. Bạn cần mình giúp gì nữa không")
        time.sleep(2)

    #----------------------News-------------------------------------#
    def News():
        baseUrl = "https://baomoi.com"
        res = requests.get(baseUrl + "/tin-moi.epi")
        soup = BeautifulSoup(res.content, "html.parser")
        heading = soup.findAll("h4", class_="story__heading")
        titles = [title.find('a').attrs["title"] for title in heading]
        AI.Speak("Sau đây là một số tin tức mới trong ngày.")
        for i in titles:
            AI.Speak(i)
            time.sleep(1)
        AI.Speak("bạn có muốn đọc tin tức không?")
        you=AI.Ear()
        if "có" in you:
            webbrowser.open(baseUrl + "/tin-moi.epi")
        else:
            AI.Speak("Nếu bạn không muốn đọc thì thôi vậy. Bạn cần mình giúp gì nữa không")
        time.sleep(2)

    #---------------------CoVid---------------------------------#
    def CoVid():
        AI.Speak("Bạn chờ một chút để mình cập nhật dữ liệu nhé.")
        res = requests.get("https://www.worldometers.info/coronavirus/#countries")
        soup = BeautifulSoup(res.content, "html.parser")
        heading = soup.find("tbody", class_="total_row_body body_world").text
        titles = heading.split("\n")
        for i in titles[:]:
            if i == "" or i[len(i) - 1].isdecimal() == False:
                titles.remove(i)
        data='''
            À có rồi. Sau đây là thống kê mới nhất về tình hình dịch corona vi rút.
            Tổng ca nhiễm: {0} 
            Số ca nhiễm mới: {1} 
            Số người thiệt mạng: {2} 
            Số người tử vong mới trong ngày: {3}
            Số người đã phục hồi: {4}
            Số trường hợp nghi nhiễm: {5}
            Số người đang được điều trị {6} 
            '''.format(titles[0].replace(",","."),titles[1][1:].replace(",","."),titles[2].replace(",","."),titles[3][1:].replace(",","."),titles[4].replace(",","."),titles[5][1:].replace(",","."),titles[6].replace(",","."))
        AI.Speak(data)
        time.sleep(1)

    #----------------------------help------------------------------------------------#
    def help():
        funct = """
                Mình có các chức năng như sau:
                1. Chào hỏi, giao tiếp 
                2. Tìm kiếm thông tin thông qua từ khóa
                3. Mở ứng dụng có sẵn
                4. Cập nhật tin tức
                5. Tìm hiểu về định danh, định nghĩa
                6. Lịch trên thiết bị
                7. Thông báo về thời tiết
                8. Kiểm tra Email
                Hết
                """
        AI.Speak(funct)
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
                    sys.exit(0)
                AI.Speak("Tớ vẫn đang lắng nghe bạn đây. Bạn cần mình giúp gì không. Nếu không hãy nói tạm biệt.")
            elif "Xin chào" in you or "xin chào" in you:
                AI.Speak("Chào bạn tớ là Rybert. Tớ có thể giúp gì cho bạn?")
            elif "tạm biệt" in you or "Tạm biệt" in you:
                AI.Speak("Tạm biệt bạn. Hẹn gặp lại.")
                sys.exit(0)
            elif "Bạn tên" in you or "Tên bạn" in you or "Tên của bạn" in you:
                AI.Speak("Tên của tớ là Rybert. Tớ có thể giúp gì cho bạn.")
            elif "giờ" in you:
                AI.Speak("Bây giờ là " + datetime.datetime.now().strftime("%H:%M:%S")) # Time
                time.sleep(1)
            elif "ngày" in you:
                AI.Speak("Hôm nay là ngày" + datetime.date.today().strftime("%d/%m/20%y"))   # Date
                time.sleep(1)
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
            elif "Google Drive" in you:
                AI.Speak("Google drive đang được mở")
                webbrowser.open("https://www.google.com/intl/vi/drive")
                time.sleep(7)
            elif "Tìm kiếm" in you or "tìm kiếm" in you:
                AI.GGSearch(you)
            elif "thời tiết" in you or "Thời tiết" in you:
                AI.Weather()
            elif "định nghĩa" in you or "ý nghĩa" in you:
                AI.Wikipedia()
            elif "đọc báo" in you or "tin tức" in you:
                AI.News()
            elif "tắt máy" in you or "shutdown" in you:
                AI.Speak("tạm biệt")
                os.system("shutdown /s")
            elif "restart" in you or "khởi động" in you:
                AI.Speak("máy tính sẽ được khởi động lại trong ít phút.")
                os.system("shutdown /r")
            elif "ngủ đông" in you:
                os.system("shutdown /h")
            elif "sleep" in you:
                os.system("shutdown /l")
            elif "email" in you or "Gmail" in you:
                AI.Email()
            elif "Corona" in you or "viêm đường hô hấp" in you or ("đại dịch" and "2019") in you:
                AI.CoVid()
            elif "chức năng" in you or "tính năng" in you:
                AI.help()
            elif "chờ" in you:
                AI.Sleep()
            else:
                AI.Speak("Tớ không hiểu cậu đang nói gì. Cậu muốn nói gì không?")

if __name__=="__main__":

    t1 = threading.Thread(target=Creat_widgets)
    t2 = threading.Thread(target=AI.main,daemon=True)
    t1.start()
    t2.start()


