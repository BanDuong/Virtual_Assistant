import speech_recognition # nhận lệnh từ speech sang text
import pyttsx3 # chuyển text sang speech
import pywin32_system32

if __name__=="__main__":
    '''robot_ear=speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        print("Robot: I'm Listening...")
        audio=robot_ear.listen(mic)
    you = robot_ear.recognize_google(audio)    
    '''
    engine = pyttsx3.init()
    engine.say("tôi tên là Bản")
    engine.runAndWait()
























